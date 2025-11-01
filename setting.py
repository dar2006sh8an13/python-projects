import os
from pathlib import Path

# ---------------- BASE DIRECTORY ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------
SECRET_KEY = 'django-insecure-your-secret-key-here'  # (auto-generated during startproject)
DEBUG = True
ALLOWED_HOSTS = []

# ---------------- INSTALLED APPS ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 👇 your custom app
    'tracker',
]

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------- URLS ----------------
ROOT_URLCONF = 'your_project.urls'  # 🔁 replace with your project folder name

# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates folder (optional)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------- WSGI ----------------
WSGI_APPLICATION = 'your_project.wsgi.application'

# ---------------- DATABASE ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- PASSWORD VALIDATION ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- LANGUAGE & TIMEZONE ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES ----------------
STATIC_URL = '/static/'

# ✅ Tell Django where to find your static files
STATICFILES_DIRS = [
    BASE_DIR / 'tracker' / 'static',   # static folder inside app
    BASE_DIR,  # include repository root so top-level `style.css` and `script.js` are served in dev
]

# (optional) for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------- MEDIA FILES (if used later) ----------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------- LOGIN & LOGOUT ----------------
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# ---------------- DEFAULT PRIMARY KEY ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
