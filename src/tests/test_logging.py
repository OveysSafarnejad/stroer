import json
import os

import pytest
from django.conf import settings
from model_bakery import baker

from apps.post.enums import ActionEnum
from apps.post.models import Comment, Post


@pytest.fixture(autouse=True)
def log_file_path():
    """Generates `log_file_path` as a fixture"""

    return os.path.join(
        settings.BASE_DIR,
        settings.MASTER_DB_LOG_FILE
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, expected',
    (
            (Post, 'Post'),
            (Comment, 'Comment'),
    )
)
def test_create_log_on_model_save_signal(model, expected, log_file_path):
    """
    Tests logs are created on `post_save` signal.

    :param Model model: Django db model
    :param str expected: created log models
    :param Fixture log_file_path: log_file_path as a fixture
    """

    baker.make(model)
    with open(log_file_path, 'r') as log_file:
        lines = [line.rstrip('\n') for line in log_file]
        last_line = json.loads(lines[-1])
        assert last_line['event'] == ActionEnum.CREATE
        assert last_line['model'] == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, expected',
    (
            (Post, 'Post'),
            (Comment, 'Comment'),
    )
)
def test_create_log_on_model_delete_signal(model, expected, log_file_path):
    """
    Tests logs are created on `post_delete` signal.

    :param Model model: Django db model
    :param str expected: created log models
    :param Fixture log_file_path: log_file_path as a fixture
    """

    model_instance = baker.make(model)
    model_instance.delete()
    with open(log_file_path, 'r') as log_file:
        lines = [line.rstrip('\n') for line in log_file]
        last_line = json.loads(lines[-1])
        assert last_line['event'] == ActionEnum.DELETE
        assert last_line['model'] == expected
