import json
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from requests import get

from apps.post.models import Post


class PostMapper:
    """
    Post mapper class.

    Takes JSONPlaceHolder post-instance data,
    returns Stroer post model compatible dictionary.
    """

    def __init__(self, post_data):
        self.user_id = post_data.get('userId')
        self.api_post_id = post_data.get('id')
        self.title = post_data.get('title')
        self.body = post_data.get('body')

    def to_dict(self):
        return self.__dict__


def get_remote_posts():
    """
    A simple generator that yields posts data.
    """

    posts_url = settings.POSTS_URL
    response = get(url=posts_url)
    posts_list = json.loads(response.content)
    for post in posts_list:
        yield post


class Command(BaseCommand):
    """
    Command that loads posts data from JSONPlaceHolder into the stroer
    database.

    Repetitive comments are not allowed.
    """

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Waiting for network")
        for post_dict in get_remote_posts():
            post_data = PostMapper(post_dict).to_dict()
            Post.objects.create_post(**post_data)

        registered_posts_count = Post.objects.count()
        self.stdout.write(
            f'{registered_posts_count} posts imported successfully.'
        )
