from rest_framework import routers

from apps.post.apis import (
    CommentViewSet,
    PostViewSet,
)

post_router = routers.DefaultRouter()
comment_router = routers.DefaultRouter()

post_router.register(
    prefix='posts',
    viewset=PostViewSet,
    basename='post'
)

comment_router.register(
    prefix='comments',
    viewset=CommentViewSet,
    basename='comment'
)
