import os

from django.conf import settings
from django.urls import reverse
from model_bakery import baker

from apps.core.tests import BaseAPITestCase
from apps.post.enums import ActionEnum
from apps.post.models import Post
from apps.post.tasks import apply_changes


class SynchronizationTaskTestCase(BaseAPITestCase):
    """Database synchronization tests"""

    def setUp(self):
        super().setUp()
        self.post = baker.make(Post, api_post_id=1)

        logfile = os.path.join(settings.BASE_DIR, settings.MASTER_DB_LOG_FILE)
        with open(logfile, 'r+') as logfile:
            logfile.truncate(0)

    def test_calls_create_on_remote_task(self):
        """Tests that scheduler runs `create_on_remote` asynchronously """

        post = baker.make(Post)

        tasks = apply_changes()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['id'], post.id)
        self.assertEqual(tasks[0]['action'], ActionEnum.CREATE)

    def test_calls_update_on_remote_task(self):
        """Tests that scheduler runs `update_on_remote` asynchronously """

        url = reverse('posts:post-detail', kwargs={
            'pk': str(self.post.id)
        })
        self.client.force_authenticate(user=self.post.user)
        post_updates = {
            'title': self.post.title,
            'body': 'updated post body'
        }
        self.client.put(url, data=post_updates)
        tasks = apply_changes()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['id'], self.post.id)
        self.assertEqual(tasks[0]['action'], ActionEnum.UPDATE)

    def test_calls_delete_on_remote_task(self):
        """Tests that scheduler runs `delete_on_remote` asynchronously """

        url = reverse('posts:post-detail', kwargs={
            'pk': str(self.post.id)
        })
        self.client.force_authenticate(user=self.post.user)
        self.client.delete(url)
        tasks = apply_changes()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['id'], self.post.id)
        self.assertEqual(tasks[0]['action'], ActionEnum.DELETE)
