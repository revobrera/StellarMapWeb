import os

bind = ['unix:/run/gunicorn.sock', '127.0.0.1:8000']
workers = 3
user = "revobrera"
group = "revobrera"
loglevel = "debug"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"

# Set the path to the Django project and settings module
django_project_path = "/home/revobrera/StellarMapWeb/StellarMapWeb"
django_settings_module = "StellarMapWeb.settings"

# Set the environment variables for the Django project
os.environ["DJANGO_SETTINGS_MODULE"] = django_settings_module
os.environ["PYTHONPATH"] = django_project_path

# Set the working directory to the Django project path
working_directory = django_project_path

# Set the Django wsgi application
django_wsgi_application = "StellarMapWeb.wsgi:application"
