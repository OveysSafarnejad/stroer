import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stroer.settings')

celery = Celery(__name__)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
celery.autodiscover_tasks()

celery.conf.beat_schedule = {
    'sync_databases': {
        'task': 'apps.post.tasks.apply_changes',
        'schedule': settings.SYNCHRONIZATION_INTERVAL
    },
}
