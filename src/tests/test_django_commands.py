from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from model_bakery import baker

from apps.post.models import Comment, Post


class FetchPostsCommandUnitTests(TestCase):
    """Tests `fetch_posts` django command"""

    @mock.patch(
        'apps.post.management.commands.fetch_posts.get'
    )
    def test_call_command(self, get_mock, *args, **kwargs):
        """
        Takes `requests.get` method as a mock and simulate its response,
        Tests `fetch_posts` commands.

        :param MagicMock get_mock: Requests.get mock
        :param args:
        :param kwargs:
        """

        mock_response = mock.Mock()
        mock_response.content = b'[\n  {\n    "userId": 1,\n    "id": 1,' \
                                b'\n    "title": "title",' \
                                b'\n    "body": "body"\n  }\n]'

        get_mock.return_value = mock_response

        out = StringIO()
        call_command(
            "fetch_posts",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, 1)


class FetchCommentsCommandUnitTests(TestCase):
    """Tests `fetch_comments` django command"""

    @mock.patch(
        'apps.post.management.commands.fetch_comments.requests.get'
    )
    def test_call_command(self, get_mock, *args, **kwargs):
        """
        Takes `requests.get` method as a mock and simulate its response,
        Tests `fetch_comments` commands.

        :param MagicMock get_mock: Requests.get mock
        :param args:
        :param kwargs:
        """
        baker.make(Post, api_post_id=1)
        mock_response = mock.Mock()
        mock_response.content = b'[\n  {\n    "postId": 1,\n    "id": 1,' \
                                b'\n    "name": "user name",' \
                                b'\n    "email": "Eliseo@gardner.biz",' \
                                b'\n    "body": "comment body"\n  }\n]'

        get_mock.return_value = mock_response

        out = StringIO()
        call_command(
            "fetch_comments",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )

        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 1)

    @mock.patch(
        'apps.post.management.commands.fetch_comments.requests.get'
    )
    def test_call_command_without_post(self, get_mock, *args, **kwargs):
        """
        Takes `requests.get` method as a mock and simulate its response,
        Tests `fetch_comments` commands if there is no post for
        fetched comments.

        :param MagicMock get_mock: Requests.get mock
        :param args:
        :param kwargs:
        """

        mock_response = mock.Mock()
        mock_response.content = b'[\n  {\n    "postId": 1,\n    "id": 1,' \
                                b'\n    "name": "user name",' \
                                b'\n    "email": "Eliseo@gardner.biz",' \
                                b'\n    "body": "comment body"\n  }\n]'

        get_mock.return_value = mock_response

        out = StringIO()
        call_command(
            "fetch_comments",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )

        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 0)
