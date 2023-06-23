from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.utilities import generate_slug
from apps.post.exceptions import CreateCommentForNonExistingPostException
from apps.user.models import User


class PostManager(models.Manager):
    """
    Post model manager

    Handles creating posts and its publisher using user_id
    """

    def create_post(self, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            user_random_slug = generate_slug(
                User,
                search_field='username',
                length=8
            )
            user = User.objects.create(
                id=user_id,
                username=user_random_slug,
                first_name=user_random_slug,
                last_name=user_random_slug,
                email=f'{user_random_slug}@mail.com'
            )
            user.set_password("secret-password")
            user.save()

        self.get_or_create(
            api_post_id=kwargs.pop('api_post_id'),
            defaults=kwargs
        )


class CommentManager(models.Manager):
    """
    Comment model manager.
    Handles creating comments.
    """

    def create_comment(self, **kwargs):

        from apps.post.models import Post
        post_id = kwargs.get('post_id')
        try:
            post = Post.objects.get(api_post_id=post_id)
            kwargs['post_id'] = post.id
        except Post.DoesNotExist:
            raise CreateCommentForNonExistingPostException(
                _("Post not found.")
            )

        self.get_or_create(
            api_comment_id=kwargs.pop('api_comment_id'),
            defaults=kwargs
        )
