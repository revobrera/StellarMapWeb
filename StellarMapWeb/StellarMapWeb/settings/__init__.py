"""
Loads the appropriate Django settings file based on the value of the ENV environment variable.

If the ENV variable is set to 'production', the settings_prod module is imported.
Otherwise, the settings_dev module is imported.
"""
import os

if os.environ.get('ENV') == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *