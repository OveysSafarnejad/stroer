import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stroer.settings')


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    django.setup()
