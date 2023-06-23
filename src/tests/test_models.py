from unittest import TestCase

import pytest
from model_bakery import baker

from apps.post.models import Comment, Post


@pytest.mark.django_db
class ModelTestCase(TestCase):
    """Models test cases."""

    def setUp(self) -> None:
        super().setUp()
        self.post = baker.make(Post)
        self.comment = baker.make(Comment)

    def test_post_model_str_returns_title(self):
        """Tests `Post` model __str__ method."""

        self.assertEqual(self.post.__str__(), self.post.title)

    def test_comment_model_str_returns_user_name_on_post(self):
        """Tests `Comment` model __str__ method."""

        self.assertEqual(
            self.comment.__str__(),
            f'{self.comment.name} comment on post {self.comment.post}'
        )
