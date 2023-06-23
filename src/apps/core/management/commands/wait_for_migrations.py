from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        all_tables = connection.introspection.table_names()
        if 'django_celery_beat_periodictasks' not in all_tables:
            raise Exception
