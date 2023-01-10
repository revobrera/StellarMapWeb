# Development-specific settings

from .settings_base import *


# load static files
STATICFILES_DIRS = [
    os.path.join(VENV_PATH, 'static'),
    os.path.join(VENV_PATH, "webApp"),
    os.path.join(VENV_PATH, "radialTidyTreeApp"),
]