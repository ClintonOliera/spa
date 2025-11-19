from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-#*-z4qsd&(f16h5r46*au%3e$6iboc&0m(kbb@gg69t0!y4tga'

DEBUG = True   # ❗ Recommended for Render (security)
                # If still debugging, set to True temporarily

ALLOWED_HOSTS = [
    'lavylotus-massage.onrender.com',
    'localhost',
    '127.0.0.1'
]

CSRF_TRUSTED_ORIGINS = [
    'https://lavylotus-massage.onrender.com',
    'http://localhost:5050'
]

# =========================
# INSTALLED APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'bookings.apps.BookingsConfig',
    'analytics',
]

# =========================
# MIDDLEWARE (correct order)
# =========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 🔥 MUST come first

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'analytics.middleware.AnalyticsMiddleware',  # 👈 Must come LAST
]

# =========================
# CORS SETTINGS (fixed)
# =========================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5050",
    "https://lavylotus-massage.onrender.com",
]

CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_CREDENTIALS = True

# =========================
# DRF + JWT
# =========================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# =========================
# POSTGRES CONFIG (correct)
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lavylotus_db',
        'USER': 'lavylotus_db_user',
        'PASSWORD': 'cBcOSCvpkRAEwCuSMZ5QS75OeLFCn0Gu',
        'HOST': 'dpg-d4b5lse3jp1c73ehdgcg-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}

# =========================
# STATIC FILES (Render fix)
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'