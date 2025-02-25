from rest_framework import status, viewsets, filters
from django.db import connection, transaction
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from django.db.utils import ProgrammingError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Schema
from .serializers import SchemaSerializer
from .utils import send_import_confirmation, clean_values, read_csv_with_fallback

SUPPORTED_FIELD_TYPES = [
    "SERIAL",
    "INTEGER",
    "BIGINT",
    "SMALLINT",
    "NUMERIC",
    "VARCHAR(255)",
    "TEXT",
    "BOOLEAN",
    "DATE",
    "TIMESTAMP",
    "JSONB",
]


class GetAllSchemaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            schemas = Schema.objects.all()
            serializer = SchemaSerializer(schemas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SchemaCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        table_name = request.data.get("table_name")
        fields = request.data.get("fields")

        if not table_name or not fields:
            return Response(
                {"error": "table_name and fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not table_name.isidentifier():
            return Response(
                {"error": "Invalid table name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sanitized_table_name = table_name.replace(" ", "").lower()

        try:
            with transaction.atomic():
                schema = Schema.objects.create(
                    table_name=sanitized_table_name, fields=fields
                )

                with connection.cursor() as cursor:
                    columns = ["id SERIAL PRIMARY KEY"]
                    for field in fields:
                        field_name = field.get("name")
                        field_type = field.get("type")
                        field_constraints = field.get("constraints")

                        if field_name == "id":
                            continue

                        if field_type not in SUPPORTED_FIELD_TYPES:
                            return Response(
                                {"error": f"Unsupported field type: {field_type}"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                        column_def = f"{field_name} {field_type}"

                        if "UNIQUE" in field_constraints:
                            column_def += " UNIQUE"
                        if "NOT NULL" in field_constraints:
                            column_def += " NOT NULL"

                        columns.append(column_def)

                    create_table_sql = f"""
                        CREATE TABLE {sanitized_table_name} (
                            {", ".join(columns)}
                        );
                    """
                    cursor.execute(create_table_sql)

                return Response(
                    {"message": f"Table {sanitized_table_name} created successfully"},
                    status=status.HTTP_201_CREATED,
                )

        except ProgrammingError as e:
            return Response(
                {"error": f"Database error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except IntegrityError as e:
            return Response(
                {"error": f"Integrity error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AddFieldsToSchemaView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, table_name):
        new_fields = request.data.get("fields")

        if not new_fields:
            return Response(
                {"error": "new_fields is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            schema = Schema.objects.get(table_name=table_name)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Schema with table name {table_name} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        for field in new_fields:
            field_name = field.get("name")
            field_type = field.get("type")
            if not field_name or not field_type:
                return Response(
                    {"error": "Each field must have a name and type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if field_type not in SUPPORTED_FIELD_TYPES:
                return Response(
                    {"error": f"Unsupported field type: {field_type}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            with transaction.atomic():
                for field in new_fields:
                    field_name = field.get("name")
                    field_type = field.get("type")
                    field_constraints = field.get("constraints")

                    add_column_sql = f"ALTER TABLE {schema.table_name} ADD COLUMN {field_name} {field_type}"

                    if "UNIQUE" in field_constraints:
                        add_column_sql += " UNIQUE"
                    if "NOT NULL" in field_constraints:
                        add_column_sql += " NOT NULL"

                    with connection.cursor() as cursor:
                        cursor.execute(add_column_sql)

                    schema.fields.append(field)
                schema.save()

                return Response(
                    {"message": f"Fields added successfully to {schema.table_name}"},
                    status=status.HTTP_200_OK,
                )

        except ProgrammingError as e:
            return Response(
                {"error": f"Database error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SchemaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["table_name"]
    ordering_fields = ["table_name"]


class DataImportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, table_name):
        file = request.FILES.get("file")
        email = request.user.email

        if not file:
            return Response(
                {"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            try:
                df = read_csv_with_fallback(file)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            schema = Schema.objects.filter(table_name=table_name).first()
            if not schema:
                return Response(
                    {"error": f"Table '{table_name}' does not exist in the schema"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            schema_fields = [field["name"] for field in schema.fields]

            if set(df.columns) != set(schema_fields):
                return Response(
                    {
                        "error": f"CSV columns do not match schema fields. Expected: {schema_fields}, Found: {df.columns.tolist()}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                cursor = connection.cursor()

                for _, row in df.iterrows():
                    cleaned_values = [
                        clean_values(row[col], column_name=col) for col in df.columns
                    ]

                    placeholders = ", ".join(["%s"] * len(df.columns))
                    columns = ", ".join(df.columns)
                    sql = (
                        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    )

                    try:
                        cursor.execute(sql, cleaned_values)
                    except Exception as e:
                        return Response(
                            {"error": f"SQL error during insert: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            send_import_confirmation(
                "Data Import Completed",
                f"The data import for table '{table_name}' has been completed successfully.",
                email,
            )
            return Response(
                {
                    "message": "Data import started. You will receive an email upon completion."
                },
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteSchemaTableView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, table_name):
        try:
            schema = Schema.objects.filter(table_name=table_name).first()

            if not schema:
                return Response(
                    {"error": f"Table '{table_name}' does not exist in the schema"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            with connection.cursor() as cursor:
                cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')

            schema.delete()

            return Response(
                {
                    "message": f"Schema table '{table_name}' and its data deleted successfully"
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
