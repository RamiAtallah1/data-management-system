import os
import sys
import psycopg2
from django.conf import settings


def ensure_db_exists():
    db_name = settings.DATABASES["default"]["NAME"]
    db_user = settings.DATABASES["default"]["USER"]
    db_password = settings.DATABASES["default"]["PASSWORD"]
    db_host = settings.DATABASES["default"]["HOST"]
    db_port = settings.DATABASES["default"]["PORT"]

    # Initialize conn to None
    conn = None

    try:
        # Connect to the default 'postgres' database to check if the target database exists
        conn = psycopg2.connect(
            dbname="postgres",  # Connect to the default 'postgres' database
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            # Create the database
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection if it was successfully created
        if conn:
            conn.close()


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_management_system.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Ensure the database exists before running any commands
    ensure_db_exists()

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
