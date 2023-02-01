import os
import sys

import django
from decouple import config
from fabric import task
from fabric.api import local, settings, abort, cd
from fabric.contrib.console import confirm

ENV = config('ENV')
VENV_PATH = config('VENV_PATH')
APP_PATH = config('APP_PATH')

sys.path.append(APP_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StellarMapWeb.settings')
django.setup()

@task
def activate_venv():
    if ENV == 'production':
        local(f'source {VENV_PATH}/bin/activate')
    else:
        local(f'source {VENV_PATH}/Scripts/activate')

@task
def git_commands():
    local('git stash')
    local('git fetch --all')
    local('git checkout master')
    local('git pull origin master')

@task
def setup_req():
    local('pip install -r ../requirements.txt')

@task
def setup_db():
    local('python manage.py sync_cassandra')

@task
def setup_config():
    local('python manage.py collectstatic --noinput')
    local('python manage.py check --deploy')

@task
def setup_crontab():
    cron_file = f"config/cron_{ENV}.txt"
    local(f"crontab < {cron_file}")

@task
def setup_test():
    with settings(warn_only=True):
        result = local('python manage.py test --verbosity 2', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

@task
def reboot_app():
    local('sudo systemctl restart nginx')
    local('sudo systemctl restart gunicorn')

@task
def prepare_deploy():
    with cd(APP_PATH):
        activate_venv()
        git_commands()
        setup_req()
        setup_db()
        setup_config()
        setup_crontab()
        setup_test()
        reboot_app()
    
