import os
from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


SECRET_KEY = os.environ["SECRET_KEY"]


ALLOWED_HOSTS = ["*"]

STATIC_ROOT = BASE_DIR + "static/production_files"

CSRF_COOKIE_SECURE = False
