from unittest.mock import mock_open

import pytest

from apps.post import utilities
from tests import sample_changes, sample_logs


@pytest.mark.django_db
@pytest.mark.parametrize(
    'log, expected',
    (
            (sample_logs.added, sample_changes.added_change_result),
            (sample_logs.added_deleted, sample_changes.added_deleted_result),
            (sample_logs.added_updated, sample_changes.added_updated_result),
            (sample_logs.deleted, sample_changes.deleted_result),
            (sample_logs.updated, sample_changes.updated_result),
            (
                    sample_logs.updated_deleted,
                    sample_changes.updated_deleted_result),
    )
)
def test_log_parser(log, expected, mocker):
    """
    Test parser generates correct changes dictionary for scheduler
    to apply on JSONPlaceHolder

    :param str log: Sample log for different scenarios happens to an instance
    :param expected: Expected result of the parser
    :param MagicMock mocker: Builtin file open function mock
    """

    mocker.patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=log
    )
    result = utilities.parse_log_file()

    assert result == expected
