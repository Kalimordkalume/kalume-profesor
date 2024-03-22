from .common import *

DEBUG = True
SECRET_KEY = "8_t#j6l#vo*!ia2p_nc+5*#t7ry-9b$h8m(lpv3rdkjsj*)i41"

ALLOWED_HOSTS = ["*"]
STATIC_URL = "frontend/"
STATICFILES_DIRS = [STATIC_URL + "css/"]
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
STATIC_ROOT = BASE_DIR / "backend/mysite/static/development_files/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Motor de la base de datos (SQLite en este ejemplo)
        "NAME": BASE_DIR / "db.sqlite3",  # Ruta de la base de datos SQLite
        # Otras opciones según el motor de base de datos utilizado:
        # 'USER': '',          # Nombre de usuario (opcional)
        # 'PASSWORD': '',      # Contraseña (opcional)
        # 'HOST': '',          # Dirección del servidor (opcional)
        # 'PORT': '',          # Puerto del servidor (opcional)
    }
}
