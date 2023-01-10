"""
Loads the appropriate Django settings file based on the value of the ENV environment variable.

If the ENV variable is set to 'production', the settings_prod module is imported.
Otherwise, the settings_dev module is imported.
"""
from decouple import config

SERVER_ENV = config('ENV')

if SERVER_ENV == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *