## Home Page:
http://localhost:8000/home_admin_hr (make sure you use the name "localhost" and not "127.0.0.1" so the Microsoft auth redirect works)

## Django Admin Page:
http://localhost:8000/admin (you can manage the users here)

## Django Super User (in the IT group)
- **Username:** superuser
- **Password:** SuperPassword1!

## If you want to start from scratch:

### Clear the DB
```sh
rm db.sqlite3
```

### Create a super user
```sh
python manage.py createsuperuser
```

### Perform migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```

### Navigate to http://localhost:8000/admin, and create an IT group- add your superuser to this group.

###Sign into the app with your superuser http://localhost:8000/home_admin_hr and navigate to the Settings page to set up your SMTP and App.

### Sync users
It only syncs groups named, and you don't need to create the groups in Django (except for IT for setup)- it will create them if they don't exist `OOL_IT`, `OOL_Admin`, `OOL_Approver`, `OOL_User`
```sh
python manage.py sync_azure_users
```
