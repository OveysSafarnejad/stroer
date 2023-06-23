import json

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from apps.core.tests import BaseAPITestCase
from apps.post.models import Post
from apps.user.models import User
from apps.user.services import get_system_user
from tests.validators.schemas import post_schema


@pytest.mark.django_db
class PostViewSetTests(BaseAPITestCase):
    """
    Post viewset endpoints tests.

    Tests all CRUD endpoints for `Post` model.
    """

    def setUp(self) -> None:
        self.user = baker.make(User)
        return super().setUp()

    def test_create_post_with_unauthenticated_user_401(self):
        url = reverse('posts:post-list')
        post = {
            'title': 'post title',
            'body': 'message',
            'user_id': self.user.id
        }

        response = self.client.post(url, data=post)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_invalid_data_400(self):
        url = reverse('posts:post-list')
        post = {
            'title': 'post title'
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data=post)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_201(self):
        url = reverse('posts:post-list')
        post = {
            'title': 'post title',
            'body': 'message',
            'user_id': self.user.id
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data=post)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)
        self.assertEqual(response['user']['user_id'], get_system_user().id)

    def test_get_all_posts_200(self):
        url = reverse('posts:post-list')
        number_of_initial_posts = 10
        baker.make(Post, _quantity=number_of_initial_posts)

        response = self.client.get(url, data={}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.check_response_schema(post_schema, response)
        self.assertEqual(len(response['results']), number_of_initial_posts)

    def test_delete_post_with_unauthenticated_user_401(self):
        post = baker.make(Post)
        url = reverse('posts:post-detail', kwargs={
            'pk': str(post.id)
        })

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_with_none_system_user_404(self):
        post = baker.make(Post, user=get_system_user())
        url = reverse('posts:post-detail', kwargs={
            'pk': str(post.id)
        })
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_system_user_204(self):
        post = baker.make(Post, user=get_system_user())
        url = reverse('posts:post-detail', kwargs={
            'pk': str(post.id)
        })
        self.client.force_authenticate(user=get_system_user())

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_post_with_unauthenticated_user_401(self):
        post = baker.make(Post)
        url = reverse('posts:post-detail', kwargs={
            'pk': str(post.id)
        })

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_with_none_system_user_404(self):
        post = baker.make(Post, user=get_system_user())
        url = reverse('posts:post-detail', kwargs={
            'pk': str(post.id)
        })
        self.client.force_authenticate(user=self.user)

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_system_user_200(self):
        post = baker.make(Post, user=get_system_user())
        url = reverse('posts:post-detail', kwargs={
            'pk': str(post.id)
        })
        self.client.force_authenticate(user=get_system_user())
        post_updates = {
            'title': post.title,
            'body': 'updated body'
        }

        response = self.client.put(url, data=post_updates)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.assertEqual(response['title'], post.title)
        self.assertEqual(response['body'], post_updates['body'])
