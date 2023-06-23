from stroer.settings.base import *  # noqa

MASTER_DB_LOG_FILE = 'logging/master_db.test.log'
BACKUP_LOG_FILE = 'logging/backup.test.log'

LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    "handlers": {
        "signals_logging_file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, MASTER_DB_LOG_FILE),  # noqa
            "level": "INFO",
            "formatter": "simple",
        },
    },
    "loggers": {
        "apps.post.receivers": {
            "level": "INFO",
            "handlers": ["signals_logging_file_handler"],
        },
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} {name} {levelname} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{message}",
            "style": "{",
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),  # noqa
        'USER': os.environ.get('POSTGRES_USER'),  # noqa
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),  # noqa
        'HOST': os.environ.get('DB_HOST'),  # noqa
        'PORT': os.environ.get('DB_PORT'),  # noqa
    }
}

SYNCHRONIZATION_INTERVAL = int(os.environ.get("SYNCHRONIZATION_INTERVAL", 5))
