# Onboard Offboard LOA

## Introduction

This project is designed to manage the onboarding, offboarding, and leave of absence (LOA) processes for employees. The web application is built using Django and integrates with Microsoft Azure for authentication.

## Features

- Employee Onboarding
- Employee Offboarding
- Leave of Absence (LOA) Management
- Administrator, IT, and User roles
- Email notifications
- Backup and Restore functionality

## Dependencies

Make sure you have the following dependencies installed before running the project:

- Python 3.12.5
- Django 5.1
- Django Allauth
- Django Social Auth
- Encrypted Fields
- Python Decouple
- Azure Identity
- Azure Keyvault Keys
- Azure Storage Blob

You can install these dependencies using pip:

```sh
pip install django==5.1
pip install django-allauth
pip install social-auth-app-django
pip install encrypted-model-fields
pip install python-decouple
pip install azure-identity
pip install azure-keyvault-keys
pip install azure-storage-blob
```

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/your-repo/onboard-offboard-loa.git
cd onboard-offboard-loa
```

### 2. Create and activate a virtual environment

```sh
python -m venv env
source env/bin/activate         # On Windows, use `env\Scripts\activate`
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Generate an encryption key

Use the following Python script to generate an encryption key:

```python
import base64
import os

key = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
print(f"Your encryption key: {key}")
```

Run the script:

```sh
python generate_key.py
```

Copy the generated key to be used in the `.env` file.

### 5. Create the `.env` file

Create a `.env` file next to your `manage.py` file with the following content:

```env
ENCRYPTION_KEY=your_generated_key_here
```

### 6. Update the Django settings

Ensure the `settings.py` file has the appropriate configurations:

```python
from decouple import config

# Load the encryption key from the .env file
FIELD_ENCRYPTION_KEY = config('ENCRYPTION_KEY')

# Other settings...
```

### 7. Run database migrations

```sh
python manage.py migrate
```

### 8. Create a superuser

```sh
python manage.py createsuperuser
```

### 9. Run the development server

```sh
python manage.py runserver
```

## Usage

Visit `http://localhost:8000` in your browser and use the superuser credentials to log in. You can then access the various functionalities of the application.

### Authentication

The application supports logging in via Microsoft Azure. Make sure to configure your Microsoft Azure credentials in the settings before attempting to log in.

## Settings Page

You can configure various settings such as SMTP configurations, Azure credentials, storage account details, and toggle SSL/TLS settings.

## Backup and Restore

Use the "Backup Now" button to create backups and the "Restore from Latest Backup" button to restore from the latest backup.

## Sync Users

Use the "Sync Users" button to synchronize users from Azure AD.
```

### Example `requirements.txt`

Make sure your `requirements.txt` includes all necessary dependencies:

```plaintext
django==5.1
django-allauth
social-auth-app-django
encrypted-model-fields
python-decouple
azure-identity
azure-keyvault-keys
azure-storage-blob
