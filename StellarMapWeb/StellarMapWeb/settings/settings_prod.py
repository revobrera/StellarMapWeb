# Production-specific settings

from .settings_base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$2-dn#6etnko4hz(wk^3nr6uesv2*)bf*r_dm1a&0*e=e#(vow'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# Set the X-Forwarded-Proto header to https if the request came through a reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Set the HSTS header to a long value to enable HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Set the Content Security Policy header to a strong value
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
