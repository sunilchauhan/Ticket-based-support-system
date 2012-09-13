import os
ROOT_PATH = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
STATIC_URL = '/static/'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'new_tracker.UserProfile'

SECRET_KEY = '7evo6=qz7mp0antr&0w!kk8lm3yuv_m6n)j*d#mu+d1rcs#s(7'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'new_tracker',
    'pagination',
)
TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.Loader',
   'django.template.loaders.app_directories.Loader',
) 

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)


ROOT_URLCONF = 'urls'

LOGIN_URL='/login/'
LOGOUT_URL='/logout/'
LOGIN_REDIRECT_URL='/index/'

ADMINS = (
)

SITE_ID = 1

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',                     
        'USER': 'root',                   
        'PASSWORD': 'asd123',                 
        'HOST': 'localhost',              
        'PORT': '3306',                     
    }
}

