from stroer.settings.base import * # noqa

# local database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'), # noqa
        'USER': os.environ.get('POSTGRES_USER'), # noqa
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'), # noqa
        'HOST': os.environ.get('DB_HOST'), # noqa
        'PORT': os.environ.get('DB_PORT'), # noqa
    }
}

# Add SQL statement logging in development
if os.environ.get('SQL_DEBUG', default="0") == '1': # noqa
    LOGGING['loggers']['django.db'] = { # noqa
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False
    }


# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': os.environ.get( # noqa
            'CACHE_BACKEND', 'django.core.cache.backends.dummy.DummyCache'
        )
    }
}


# set up Django Debug Toolbar if installed
try:
    import debug_toolbar  # noqa

    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware') # noqa
    INSTALLED_APPS.append('debug_toolbar') # noqa
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'debug_toolbar.middleware.show_toolbar',
    }
except ImportError:
    ...
