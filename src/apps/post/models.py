from django.db import models

from apps.core.models import BaseModel
from apps.post.managers import CommentManager, PostManager


class Post(BaseModel):
    api_post_id = models.IntegerField(
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    body = models.TextField(
        null=False,
        blank=False
    )

    user = models.ForeignKey(
        'user.User',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    objects = PostManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

        indexes = [
            models.Index(fields=['api_post_id', 'title'])
        ]

    def __str__(self):
        return self.title


class Comment(BaseModel):
    api_comment_id = models.IntegerField(
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    email = models.EmailField()
    body = models.TextField(
        null=False,
        blank=False
    )

    post = models.ForeignKey(
        'post.Post',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    objects = CommentManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['api_comment_id', 'post'])
        ]

    def __str__(self):
        return f'{self.name} comment on post {self.post}'
