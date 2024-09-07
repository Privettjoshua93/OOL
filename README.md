## Home Page:
http://localhost:8000/home_admin_hr (make sure you use the name "localhost" and not "127.0.0.1" so the Microsoft auth redirect works)

## Django Admin Page:
http://localhost:8000/admin (you can manage the users here)

pip install django
pip install azure-identity
pip install azure-keyvault-secrets
pip install environ
pip install azure-storage-blob

### Perform migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```
### Create a super user
```sh
python manage.py createsuperuser
```

### Navigate to http://localhost:8000/admin, and create an IT group- add your superuser to this group.

### Sign into the app with your superuser http://localhost:8000/home_admin_hr and navigate to the Settings page to set up your SMTP and App and sync your users.
