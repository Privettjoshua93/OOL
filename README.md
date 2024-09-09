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

```sh
pip install django==5.1
pip install django-allauth
pip install social-auth-app-django
pip install encrypted-model-fields
pip install python-decouple
pip install azure-identity
pip install azure-keyvault-keys
pip install azure-storage-blob
pip install django-encrypted-model-fields
```

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/Privettjoshua93/OOL.git
```

### 2. Create and activate a virtual environment

```sh
python -m venv env
.env\Scripts\activate
```

### 3. Generate an encryption key

Use the following Python script to generate an encryption key:

```python
import base64
import os

key = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
print(f"Your encryption key: {key}")
```

Copy the generated key to be used in the `.env` file.

### 4. Create the `.env` file

Create a `.env` file next to your `manage.py` file with the following content:

```env
ENCRYPTION_KEY = 'your_generated_key_here'
```

### 5. Run database migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```sh
python manage.py createsuperuser
```

### 7. Run the development server

```sh
python manage.py runserver
```

### 8. Sign into http://localhost:8000/admin with your superuser. Create a group named IT. Place your user in the group.

### 9. Navigate to http://localhost:8000/home_admin_hr with your superuser. Navigate to Settings. Fill out the required information and click Save. Sync your users. You may now sign in with Microsoft.

