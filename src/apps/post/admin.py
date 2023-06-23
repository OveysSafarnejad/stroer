from django.contrib import admin

from apps.core.admin import ModelAdminBase
from apps.post.models import Post, Comment
from apps.user.models import User


class CommentAdminInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(ModelAdminBase):
    list_display = ('title', 'user_id', 'comments')
    list_display_links = ('id', 'title',)
    raw_id_fields = ('user',)
    list_per_page = 10
    inlines = [CommentAdminInline, ]

    def comments(self, entity):
        return self.get_list_page(Comment, 'tap to watch', post=entity.id)

    def user_id(self, entity):
        return self.get_detail_page(User, entity.user_id)


@admin.register(Comment)
class CommentAdmin(ModelAdminBase):
    list_display = ('name', 'email', 'post_id',)
    list_display_links = ('name', 'email',)
    raw_id_fields = ('post',)
    list_per_page = 10

    def post_id(self, entity):
        return self.get_detail_page(Post, entity.post_id)
