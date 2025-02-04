# Data Management System

## Overview

The Data Management System is a backend solution for managing data schemas, performing CRUD operations, and handling large data imports efficiently. This system provides secure, flexible APIs for managing data tables, importing data, and more.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.12
- Django 5
- PostgreSQL 16
- Node.js (for Vue.js frontend build)
- npm (for frontend dependencies)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/RamiAtallah1/data-management-system.git
cd data-management-system
```

### 2. Create and activate the virtual environment (if not already done)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Install frontend dependencies

Navigate to the `frontend` directory and install the required packages.

```bash
cd frontend
npm install
```

### 5. Environment Configuration

Create a `.env` file in the root directory of your project. This file will store sensitive configuration data. Here is the template for the `.env` file:

```env
# Django settings
SECRET_KEY=your-secret-key-here  # Replace with your actual secret key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1  # Add your allowed hosts here

# Database settings
DB_NAME=data_management_system  # Replace with your database name
DB_USER=postgres  # Replace with your database user
DB_PASSWORD=yourpassword  # Replace with your database password
DB_HOST=localhost  # Replace with your database host
DB_PORT=5432  # Replace with your database port if different

# Email settings
EMAIL_HOST=smtp.gmail.com  # Replace with your email host
EMAIL_PORT=587  # Replace with your email SMTP port
EMAIL_USE_TLS=True  # Set to True if using TLS
EMAIL_HOST_USER=your-email@gmail.com  # Replace with your email address
EMAIL_HOST_PASSWORD=your-email-password  # Replace with your email password

# JWT settings
ACCESS_TOKEN_LIFETIME=30  # Expiry in days for access tokens
REFRESH_TOKEN_LIFETIME=30  # Expiry in days for refresh tokens
```

### 6. Run Migrations

To set up the database schema, run the following command:

```bash
python manage.py migrate
```

### 7. Build the Vue.js Frontend

Go back to the `frontend` directory and build the Vue.js app:

```bash
cd frontend
npm run build
```

### 10. Run the Development Server

To run the Django development server:

```bash
python manage.py runserver
```

The frontend should now be accessible from the built static files, and the backend API will be running at `http://localhost:8000/`.

---

## `.env` Configuration

The `.env` file contains sensitive data like your Django secret key, database configuration, and email credentials. Make sure to replace the placeholder values in the `.env` file with your actual values.

Here’s a breakdown of what to include in your `.env`:

- **Django settings:**

  - `SECRET_KEY`: Your Django secret key. This is a unique value used for cryptographic signing. You should generate a new secret key (don't use the one from the template).
  - `DEBUG`: Set this to `True` for development. Set it to `False` in production for security reasons.
  - `ALLOWED_HOSTS`: This should be a comma-separated list of hosts that your Django app is allowed to serve. For local development, `localhost` and `127.0.0.1` are sufficient.

- **Database settings:**

  - `DB_NAME`: The name of your PostgreSQL database.
  - `DB_USER`: The username for your PostgreSQL database.
  - `DB_PASSWORD`: The password for your PostgreSQL database.
  - `DB_HOST`: The host of your PostgreSQL database, typically `localhost`.
  - `DB_PORT`: The port where your PostgreSQL database is running, typically `5432`.

- **Email settings (for sending notifications):**

  - `EMAIL_HOST`: The email provider's SMTP host (e.g., `smtp.gmail.com` for Gmail).
  - `EMAIL_PORT`: The SMTP port (usually `587` for Gmail with TLS).
  - `EMAIL_USE_TLS`: Set to `True` if your email service uses TLS.
  - `EMAIL_HOST_USER`: The email address you'll be sending emails from.
  - `EMAIL_HOST_PASSWORD`: The password for your email account (or app-specific password if using Gmail with 2FA).

- **JWT settings:**
  - `ACCESS_TOKEN_LIFETIME`: The lifetime (in days) of access tokens.
  - `REFRESH_TOKEN_LIFETIME`: The lifetime (in days) of refresh tokens.
