Home page:
http://localhost:8000/home_admin_hr (make sure you use the name "localhost" and not "127.0.0.1" so the Microsoft auth redirect works)

Django Admin page:
http://localhost:8000/admin (you can manage the users here)


Django Super User (in the IT group)
superuser
SuperPassword1!


If you want to start from scratch:

#Clear the DB
python manage.py flush

#Create a super user
python manage.py createsuperuser

Perform migrations:
python manage.py makemigrations
python manage.py migrate

Navigate to http://localhost:8000/admin, and create your four groups: IT, Admin, Approver, User

#Sync users (this is a little buggy at the moment- duplicates may show up after some amount of time)
#It only syncs groups named OOL_IT, OOL_Admin, OOL_Approver, OOL_User
python manage.py sync_azure_users

Navigate to http://localhost:8000/admin, and add the IT group to your super user.

Navigate to http://localhost:8000/home_admin_hr, and sign in with your super user.
Go to Settings and set up your App details, along with your SMTP creds. (Make sure to allow authenticated smtp on your user)
