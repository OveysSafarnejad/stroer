from rest_framework import serializers

from apps.post.models import Comment, Post
from apps.user.services import get_system_user


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user',)
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        # request.user override with system-user
        validated_data["user"] = get_system_user()
        return super().create(validated_data)

    @staticmethod
    def get_user(instance):
        return dict(
            user_id=instance.user_id,
            email=instance.user.email
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'post', 'name', 'email')
        read_only_fields = ('id', 'name', 'email')

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data['name'] = user.full_name
        validated_data['email'] = user.email
        comment = super().create(validated_data)
        return comment

    def to_representation(self, instance):
        repr_data = super().to_representation(instance)
        repr_data['post'] = PostSerializer(instance.post).data
        return repr_data


class CommentListSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id')
    api_post_id = serializers.IntegerField(source='post.api_post_id')

    class Meta:
        model = Comment
        fields = (
            'id',
            'api_comment_id',
            'post_id',
            'api_post_id',
            'name',
            'email',
            'body'
        )


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'post', 'name', 'email',)
        read_only_fields = ('id', 'post', 'name', 'email',)

    def to_representation(self, instance):
        repr_data = super().to_representation(instance)
        repr_data['post'] = PostSerializer(instance.post).data
        return repr_data
