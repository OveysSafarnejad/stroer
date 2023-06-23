from django.db.models import QuerySet

from apps.post.models import (
    Comment,
    Post,
)
from apps.user.models import User


def get_posts() -> QuerySet:
    """Fetch all posts and its related fields from the database."""

    return Post.objects.select_related(
        'user'
    ).only(
        'id',
        'title',
        'body',
        'api_post_id',
        'user__id',
        'user__email'
    )


def get_user_posts(user: User) -> QuerySet:
    """Fetch all user's post."""

    return Post.objects.filter(
        user=user
    ).select_related(
        'user'
    ).only(
        'id',
        'title',
        'body',
        'api_post_id',
        'user__id',
        'user__email'
    )


def get_comments(post_id: int = None) -> QuerySet:
    """
    Fetch all comments and its related fields from the database.

    :param int post_id: Post_id for filtering comments

    :rtype: QuerySet
    """

    queryset = Comment.objects.select_related(
        'post'
    )

    if post_id:
        queryset = queryset.filter(
            post_id=post_id
        )

    return queryset


def get_user_comments(user: User) -> QuerySet:
    """
    Takes user instance, returns all user comments.

    :param user: comment publisher

    :rtype: QuerySet
    """

    return Comment.objects.filter(
        email=user.email
    ).select_related(
        'post'
    )
