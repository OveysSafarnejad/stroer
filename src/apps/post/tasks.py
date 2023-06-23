from django.conf import settings
from rest_framework import status

from apps.core import cache_manager
from apps.post.enums import ActionEnum
from apps.post.exceptions import JSONPlaceHolderResponseException
from apps.post.receivers import create_log_record
from apps.post.request_handler import RequestHandler
from apps.post.utilities import parse_log_file
from stroer.celery_conf import celery

POST_URL: object = settings.POSTS_URL


@celery.task()
def create_on_remote(resource: int, body: dict):
    """
    Takes information about created data on stroer, reflects them on the
    JSONPlaceHolder.
    Also, it returns compact change data to the log file on
    request failure.

    :param int resource: Instance_id
    :param dict body: Instance_data

    :rtype: None
    """

    handler = RequestHandler(retries=3)
    try:
        response = handler.try_post(url=POST_URL, body=body)
    except JSONPlaceHolderResponseException:
        create_log_record(
            instance_id=resource,
            instance_data=body,
            model="Post",
            action=ActionEnum.CREATE
        )
    else:
        if response.status_code == status.HTTP_201_CREATED:
            if settings.PROFILE == 'test':
                cache_manager.set_key(
                    key=resource,
                    value="CREATED"
                )
        else:
            create_log_record(
                instance_id=resource,
                instance_data=body,
                model="Post",
                action=ActionEnum.CREATE
            )


@celery.task()
def update_on_remote(resource: int, body: dict):
    """
    Takes information about updated data on stroer, reflects them on the
    JSONPlaceHolder.
    Also, it returns compact change data to the log file on
    request failure.

    :param int resource: Instance_id
    :param dict body: Instance_data

    :rtype: None
    """

    handler = RequestHandler(retries=3)
    put_url = POST_URL + f'/{resource}'
    try:
        response = handler.try_put(url=put_url, body=body)
    except JSONPlaceHolderResponseException:
        create_log_record(
            instance_id=resource,
            instance_data=body,
            action=ActionEnum.UPDATE,
            model="Post"
        )
    else:
        if response.status_code == status.HTTP_200_OK:
            if settings.PROFILE == 'test':
                cache_manager.set_key(
                    key=resource,
                    value="UPDATED"
                )
        else:
            create_log_record(
                instance_id=resource,
                instance_data=body,
                action=ActionEnum.UPDATE,
                model="Post"
            )


@celery.task()
def delete_from_remote(resource: int):
    """
    Takes information about deleted data on stroer, reflects them on the
    JSONPlaceHolder.
    Also, it returns compact change data to the log file on
    request failure.

    :param int resource: Instance_id

    :rtype: None
    """

    handler = RequestHandler(retries=3)
    delete_url = POST_URL + f'/{resource}'
    try:
        response = handler.try_delete(url=delete_url)
    except JSONPlaceHolderResponseException:
        create_log_record(
            instance_id=resource,
            instance_data={},
            action=ActionEnum.DELETE,
            model="Post"
        )
    else:
        if response.status_code == status.HTTP_200_OK:
            if settings.PROFILE == 'test':
                cache_manager.set_key(
                    key=resource,
                    value="DELETED"
                )
        else:
            create_log_record(
                instance_id=resource,
                instance_data={},
                action=ActionEnum.DELETE,
                model="Post"
            )


@celery.task()
def apply_changes():
    """
    Parse the log file periodically and register async celery tasks in response
    to changes.
    (Since JSONPlaceHolder does not have endpoints for comments
    manipulations, changes on the comment model can't be reflected.)

    :rtype: Dictionary
    """

    changes = parse_log_file()
    tasks = []

    for key, value in changes.items():
        match value['action']:

            case ActionEnum.CREATE:

                post_data = dict(
                    title=value['update']['title'],
                    body=value['update']['body'],
                    userId=value['update']['user_id']
                )
                task = create_on_remote.delay(
                    resource=key,
                    body=post_data,
                )
                tasks.append(dict(
                    action=ActionEnum.CREATE,
                    id=key,
                    task_id=task.id
                ))

            case ActionEnum.UPDATE:
                post_data = dict(
                    id=value["update"]["api_post_id"],
                    title=value['update']['title'],
                    body=value['update']['body'],
                    userId=value['update']['user_id']
                )

                task = update_on_remote.delay(
                    resource=value["update"]["api_post_id"],
                    body=post_data
                )
                tasks.append(dict(
                    action=ActionEnum.UPDATE,
                    id=key,
                    task_id=task.id
                ))

            case ActionEnum.DELETE:
                task = delete_from_remote.delay(
                    resource=value["update"]["api_post_id"]
                )
                tasks.append(dict(
                    action=ActionEnum.DELETE,
                    id=key,
                    task_id=task.id
                ))

    return tasks
