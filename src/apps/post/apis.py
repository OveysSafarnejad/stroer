from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.pagination import MediumPagination, paginate
from apps.core.viewsets import CoreViewSet
from apps.post.models import Comment, Post
from apps.post.querysets import (
    get_user_posts,
    get_posts,
    get_user_comments,
    get_comments,
)
from apps.post.serializers import (
    CommentSerializer,
    CommentListSerializer,
    CommentUpdateSerializer,
    PostSerializer,
)


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    CoreViewSet
):
    """
    Post 'ModelViewSet' using mixins and CoreViewSet

    Accepted methods: list, retrieve, post, put, delete
    """

    model = Post
    pagination_class = MediumPagination

    permissions = {
        'create': IsAuthenticated,
        'list': None,
        'retrieve': None,
        'destroy': IsAuthenticated,
        'update': IsAuthenticated,
    }

    serializers = {
        'create': PostSerializer,
        'list': PostSerializer,
        'retrieve': PostSerializer,
        'update': PostSerializer,
        'partial_update': PostSerializer,
        'comments': CommentListSerializer,
    }

    def get_queryset(self):
        if self.request.method in ['DELETE', 'PUT']:
            return get_user_posts(user=self.request.user)
        else:
            return get_posts()

    @paginate
    @action(methods=['GET'], detail=True, url_path='comments')
    def comments(self, request, *args, **kwargs):  # noqa
        post = self.get_object()
        comments = get_comments(post.id)
        return comments


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    CoreViewSet
):
    """
    Comment 'ModelViewSet' using mixins and CoreViewSet

    Accepted methods: list, retrieve, post, put, delete
    """
    model = Comment
    pagination_class = MediumPagination

    permissions = {
        'create': IsAuthenticated,
        'list': None,
        'retrieve': None,
        'destroy': IsAuthenticated,
        'update': IsAuthenticated,
    }

    serializers = {
        'create': CommentSerializer,
        'list': CommentListSerializer,
        'retrieve': CommentSerializer,
        'update': CommentUpdateSerializer,
        'partial_update': CommentUpdateSerializer
    }

    def get_queryset(self):
        if self.request.method in ['DELETE', 'PUT']:
            return get_user_comments(user=self.request.user)
        else:
            post_id = self.request.GET.get('postId', None)
            return get_comments(post_id=post_id)
