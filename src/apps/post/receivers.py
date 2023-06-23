import json
import logging

from django.db.models.signals import (
    post_save,
    post_delete,
)
from django.dispatch import receiver

from apps.post.enums import ActionEnum
from apps.post.models import (
    Comment,
    Post,
)

logger = logging.getLogger(__name__)


class PostLogMapper:
    """Create log data used by logger for post instance"""

    def __init__(self, instance):
        self.user_id = instance.user_id
        self.api_post_id = instance.api_post_id or None
        self.title = instance.title
        self.body = instance.body

    def to_dict(self):
        return self.__dict__


class CommentLogMapper:
    """Create log data used by logger for comment instance"""

    def __init__(self, instance):
        self.api_comment_id = instance.api_comment_id
        self.name = instance.name
        self.email = instance.email
        self.api_comment_id = instance.api_comment_id or None
        self.body = instance.body
        self.post_id = instance.post.id

    def to_dict(self):
        return self.__dict__


@receiver(
    signal=post_save,
    sender=Post,
    dispatch_uid='save_post_call_back'
)
@receiver(
    signal=post_save,
    sender=Comment,
    dispatch_uid='save_comment_call_back'
)
def save_model_callback(sender, instance, created, **kwargs):
    """
    Save model receiver, which takes Post & Comment instance,
    and logs its data for scheduler to update the remote JSONPlaceHolder
    database.

    :param sender: Post or Comment
    :param instance:  Model instance
    :param created: boolean value indicated updating or creation
    :param kwargs: other signal required parameters

    :rtype: None
    """

    if sender is Post:
        instance_data = PostLogMapper(instance).to_dict()
    else:
        instance_data = CommentLogMapper(instance).to_dict()

    if created:
        create_log_record(
            instance_id=instance.id,
            instance_data=instance_data,
            action=ActionEnum.CREATE,
            model=sender.__name__
        )

    else:
        create_log_record(
            instance_id=instance.id,
            instance_data=instance_data,
            action=ActionEnum.UPDATE,
            model=sender.__name__
        )


@receiver(
    signal=post_delete,
    sender=Post,
    dispatch_uid='delete_post_call_back'
)
@receiver(
    signal=post_delete,
    sender=Comment,
    dispatch_uid='delete_comment_call_back'
)
def delete_model_callback(sender, instance, **kwargs):
    """
    Delete model receiver, which takes Post & Comment instance,
    and logs its data for scheduler to update the remote JSONPlaceHolder
    database.

    :param sender: Post or Comment
    :param instance:  Model instance
    :param kwargs: other signal required parameters

    :rtype: None
    """

    if sender is Post:
        instance_data = PostLogMapper(instance).to_dict()
    else:
        instance_data = CommentLogMapper(instance).to_dict()

    create_log_record(
        instance_id=instance.id,
        instance_data=instance_data,
        action=ActionEnum.DELETE,
        model=sender.__name__
    )


def create_log_record(instance_id, instance_data, action, model):
    log_message = {
        'event': action,
        'model': model,
        'instance_id': instance_id,
        'instance_data': instance_data,
    }
    logger.info(json.dumps(log_message, default=str))
