"""
WSGI config for stroer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import pathlib
from django.core.wsgi import get_wsgi_application
from os.path import basename, dirname

import dotenv


BASE_DIR = pathlib.Path(__file__).parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
dotenv.read_dotenv(str(ENV_PATH))

settings_package = basename(dirname(__file__)) + '.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_package)
application = get_wsgi_application()
