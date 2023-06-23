import json

import pytest
from django.urls import reverse
from django.utils.http import urlencode
from model_bakery import baker
from rest_framework import status

from apps.core.tests import BaseAPITestCase
from apps.post.models import Comment, Post
from apps.user.models import User
from tests.validators.schemas import comment_schema


@pytest.mark.django_db
class CommentViewSetTests(BaseAPITestCase):
    """
    Comment viewset endpoints tests.

    Tests all CRUD endpoints for `Comment` model.
    """

    def setUp(self) -> None:
        self.user = baker.make(User)
        return super().setUp()

    def test_create_comment_with_unauthenticated_user_401(self):
        url = reverse('comments:comment-list')

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_invalid_data_400(self):
        url = reverse('comments:comment-list')
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_201(self):
        url = reverse('comments:comment-list')

        post = baker.make(Post)
        comment = {
            'body': 'comment text',
            'post': post.id
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data=comment)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)
        self.assertEqual(response['body'], comment['body'])
        self.assertEqual(response['post']['id'], post.id)
        self.assertEqual(response['email'], self.user.email)

    def test_get_all_comments_200(self):
        url = reverse('comments:comment-list')
        post = baker.make(Post)
        number_of_initial_comment = 10
        baker.make(Comment, post=post, _quantity=number_of_initial_comment)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.check_response_schema(comment_schema, response)
        self.assertEqual(len(response['results']), number_of_initial_comment)

    def test_get_all_comments_for_special_post_200(self):
        url = reverse('comments:comment-list')
        number_of_initial_comment = 10
        post = baker.make(Post)
        baker.make(Comment, post=post, _quantity=number_of_initial_comment)
        post2 = baker.make(Post)
        baker.make(Comment, post=post2, _quantity=number_of_initial_comment)
        url = '{}?{}'.format(url, urlencode({'postId': post.id}))

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.assertEqual(len(response['results']), number_of_initial_comment)

    def test_delete_comment_with_unauthenticated_user_401(self):
        comment = baker.make(Comment)

        url = reverse('comments:comment-detail', kwargs={
            'pk': str(comment.id)
        })

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_unauthorized_404(self):
        comment = baker.make(Comment)
        url = reverse('comments:comment-detail', kwargs={
            'pk': str(comment.id)
        })
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_authorized_204(self):
        comment = baker.make(Comment, email=self.user.email)
        url = reverse('comments:comment-detail', kwargs={
            'pk': str(comment.id)
        })
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_comment_with_unauthenticated_user_401(self):
        comment = baker.make(Comment)
        url = reverse('comments:comment-detail', kwargs={
            'pk': str(comment.id)
        })

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_comment_unauthorized_404(self):
        comment = baker.make(Comment)
        url = reverse('comments:comment-detail', kwargs={
            'pk': str(comment.id)
        })
        self.client.force_authenticate(user=self.user)

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment_204(self):
        comment = baker.make(Comment, email=self.user.email)
        url = reverse('comments:comment-detail', kwargs={
            'pk': str(comment.id)
        })
        self.client.force_authenticate(user=self.user)
        comment_updates = {
            'body': 'updated body'
        }

        response = self.client.put(url, data=comment_updates)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.assertEqual(response['email'], self.user.email)
        self.assertEqual(response['body'], comment_updates['body'])
