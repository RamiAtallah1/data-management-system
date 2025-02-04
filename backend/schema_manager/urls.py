from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GetAllSchemaView,
    SchemaCreateView,
    AddFieldsToSchemaView,
    SchemaViewSet,
    DataImportView,
    DeleteSchemaTableView,
)

router = DefaultRouter()
router.register(r"schemas", SchemaViewSet, basename="schema")

urlpatterns = [
    path("", GetAllSchemaView.as_view(), name="get-all-schemas"),
    path("create/", SchemaCreateView.as_view(), name="schema-create"),
    path(
        "add-fields/<str:table_name>/",
        AddFieldsToSchemaView.as_view(),
        name="add-fields",
    ),
    path(
        "delete/<str:table_name>/",
        DeleteSchemaTableView.as_view(),
        name="delete-schema",
    ),
    path("import/<str:table_name>/", DataImportView.as_view(), name="data-import"),
    path("", include(router.urls)),
]
