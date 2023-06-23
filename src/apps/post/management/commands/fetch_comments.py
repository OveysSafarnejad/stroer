import json
from typing import Any

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.post.exceptions import CreateCommentForNonExistingPostException
from apps.post.models import Comment


class CommentMapper:
    """
    Comment mapper class.

    Takes JSONPlaceHolder comment-instance data,
    returns Stroer Comment model compatible dictionary.
    """

    def __init__(self, comment_data):
        self.api_comment_id = comment_data.get('id')
        self.post_id = comment_data.get('postId')
        self.name = comment_data.get('name')
        self.email = comment_data.get('email')
        self.body = comment_data.get('body')

    def to_dict(self):
        return self.__dict__


def get_remote_comments():
    """
    A simple generator that yields comments data.
    """

    comments_url = settings.COMMENTS_URL
    response = requests.get(url=comments_url)
    comment_list = json.loads(response.content)
    for comment in comment_list:
        yield comment


class Command(BaseCommand):
    """
     Command that loads comment data from JSONPlaceHolder into the stroer
     database.

     Comments for non-existing posts will be skipped and repetitive comments
     are not allowed
     """

    def handle(self, *args: Any, **options: Any):

        self.stdout.write("Waiting for network")
        for comment_dict in get_remote_comments():
            comment_data = CommentMapper(comment_dict).to_dict()
            try:
                Comment.objects.create_comment(**comment_data)
            except CreateCommentForNonExistingPostException:
                self.stdout.write(
                    f'skipping comments for post with id {comment_data["post_id"]}'
                )

        registered_comments_count = Comment.objects.count()
        self.stdout.write(
            f'{registered_comments_count} comments imported successfully.'
        )
