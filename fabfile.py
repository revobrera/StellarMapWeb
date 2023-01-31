from decouple import config
from fabric import task

env_file = 'StellarMapWeb/StellarMapWeb/.env'

ENV = config('ENV', cast=str, source=env_file)
VENV_PATH = config('VENV_PATH', cast=str, source=env_file)

@task
def activate_venv(c):
    if ENV == 'production':
        c.run(f'source {VENV_PATH}/bin/activate')
    else:
        c.run(f'source {VENV_PATH}/Scripts/activate')

@task
def git_commands(c):
    c.run('git fetch --all')
    c.run('git pull origin master')

@task
def setup_req(c):
    c.run('pip install -r StellarMapWeb/requirements.txt')

@task
def setup_db(c):
    c.run('python StellarMapWeb/manage.py sync_cassandra')

@task
def setup_config(c):
    c.run('python StellarMapWeb/manage.py collectstatic --noinput')
    c.run('python StellarMapWeb/manage.py check --deploy')
    c.run('python StellarMapWeb/manage.py test --verbosity 2')

@task
def setup_crontab(c):
    cron_file = f"StellarMapWeb/config/cron_{ENV}.txt"
    c.run(f"crontab < {cron_file}")

@task
def reboot_app(c):
    c.run('sudo systemctl restart nginx')
    c.run('sudo systemctl restart gunicorn')

@task
def run_all_commands(c):
    activate_venv(c)
    git_commands(c)
    setup_req(c)
    setup_db(c)
    setup_config(c)
    setup_crontab(c)
    reboot_app(c)
    
