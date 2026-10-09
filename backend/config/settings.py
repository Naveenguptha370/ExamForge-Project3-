"""
ExamForge M2 — Django Settings
================================
Full production-ready settings for Student Management,
Academic Management, and Subject & Exam Registration modules.

Integrates with M1's authentication system via the accounts app.
"""

import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import structlog

# ─── Base Directory ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Security ────────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-examforge-m2')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ─── Application Definition ──────────────────────────────────────────────────────
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'debug_toolbar',
]

# M1 apps (already existing — do not reimplement)
M1_APPS = [
    'accounts',       # M1: Authentication & User Management
    'faculty',        # M1: Faculty Management
]

# M2 apps (owned by Member 2)
M2_APPS = [
    'students',       # M2: Student Management
    'academics',      # M2: Academic Management
    'registrations',  # M2: Subject & Exam Registration
]

# M3 apps (M3 owns — referenced for integration)
M3_APPS = [
    # 'examinations',   # M3: Examination Config & Timetable (activate when M3 is ready)
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + M1_APPS + M2_APPS + M3_APPS

# ─── Middleware ──────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'students.middleware.StudentRequestLoggingMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ─── Templates ───────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ─── Database ────────────────────────────────────────────────────────────────────
db_engine = config('DB_ENGINE', default='django.db.backends.postgresql')
db_config = {
    'ENGINE': db_engine,
    'NAME': config('DB_NAME', default='examforge_db'),
    'USER': config('DB_USER', default='examforge_user'),
    'PASSWORD': config('DB_PASSWORD', default='password'),
    'HOST': config('DB_HOST', default='localhost'),
    'PORT': config('DB_PORT', default='5432'),
    'CONN_MAX_AGE': 60,
}
if 'postgresql' in db_engine:
    db_config['OPTIONS'] = {'connect_timeout': 10}

DATABASES = {
    'default': db_config
}

# ─── Custom User Model (Reusing M1) ─────────────────────────────────────────────
AUTH_USER_MODEL = config('AUTH_USER_MODEL', default='accounts.User')

# ─── Password Validators ─────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalization ────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ─── Static & Media Files ────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / config('STATIC_ROOT', default='staticfiles/')
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / config('MEDIA_ROOT', default='media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Django REST Framework ───────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.StandardResultsPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'EXCEPTION_HANDLER': 'config.exceptions.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '200/minute',
        'student_import': '5/minute',
        'bulk_registration': '10/minute',
    },
}

# ─── JWT Configuration ───────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60, cast=int)
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7, cast=int)
    ),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': config('JWT_ALGORITHM', default='HS256'),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# ─── CORS Configuration ──────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ─── DRF Spectacular (API Documentation) ────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE': 'ExamForge M2 API',
    'DESCRIPTION': (
        'REST API for ExamForge Member 2 modules: '
        'Student Management, Academic Management, and Subject & Exam Registration.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'students', 'description': 'Student Management endpoints'},
        {'name': 'academics', 'description': 'Academic Management endpoints'},
        {'name': 'registrations', 'description': 'Subject & Exam Registration endpoints'},
        {'name': 'departments', 'description': 'Department Management'},
        {'name': 'courses', 'description': 'Course Management'},
        {'name': 'branches', 'description': 'Branch Management'},
        {'name': 'semesters', 'description': 'Semester Management'},
        {'name': 'subjects', 'description': 'Subject Management'},
        {'name': 'academic-years', 'description': 'Academic Year Management'},
    ],
}

# ─── Cache ───────────────────────────────────────────────────────────────────────
try:
    import django_redis  # noqa: F401
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://localhost:6379/0'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'TIMEOUT': 300,
        }
    }
except ImportError:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'examforge-m2-locmem',
        }
    }

# ─── Celery (for bulk import tasks) ─────────────────────────────────────────────
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/2')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes max per task

# ─── Logging ─────────────────────────────────────────────────────────────────────
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'examforge_m2.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'student_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'students.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'academic_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'academics.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'registration_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'registrations.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'students': {
            'handlers': ['console', 'student_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'academics': {
            'handlers': ['console', 'academic_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'registrations': {
            'handlers': ['console', 'registration_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# ─── File Upload Settings ────────────────────────────────────────────────────────
MAX_UPLOAD_SIZE = config('MAX_UPLOAD_SIZE_MB', default=10, cast=int) * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
ALLOWED_IMPORT_EXTENSIONS = ['.csv']
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']

# ─── Student Import Settings ─────────────────────────────────────────────────────
STUDENT_IMPORT = {
    'MAX_ROWS': config('STUDENT_IMPORT_MAX_ROWS', default=5000, cast=int),
    'BATCH_SIZE': config('STUDENT_IMPORT_BATCH_SIZE', default=100, cast=int),
    'REQUIRED_COLUMNS': [
        'roll_number', 'full_name', 'email', 'department_code',
        'course_code', 'semester_number', 'academic_year',
    ],
    'OPTIONAL_COLUMNS': ['branch_code', 'phone', 'admission_date', 'gender', 'date_of_birth'],
}

# ─── Registration Settings ───────────────────────────────────────────────────────
REGISTRATION = {
    'ALLOW_LATE_REGISTRATION': config('ALLOW_LATE_REGISTRATION', default=False, cast=bool),
    'DEFAULT_STATUS': config('DEFAULT_REGISTRATION_STATUS', default='registered'),
    'CONCURRENT_REGISTRATION_PROTECTION': True,
    'MAX_BULK_REGISTRATION_ROWS': 1000,
}

# ─── Debug Toolbar ───────────────────────────────────────────────────────────────
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# ─── Security Settings (Production) ─────────────────────────────────────────────
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
