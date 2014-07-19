import os


CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'localhost',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('var', 'database.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}
DEBUG = True
INSTALLED_APPS = (
    'cashmere',
    'corsheaders',
    'floppyforms',
    'mptt',
    'rest_framework',
    'south',
    'templateaddons',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
)
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'cashmere.urls'
SECRET_KEY = 'not a secret'
STATIC_URL = 'http://localhost:8001/'
TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
]
USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = 'fr'
LANGUAGES = [('fr', 'fr')]
