import json
import os

from django.conf import settings

from apps.post.enums import ActionEnum

LOG_FILE = os.path.join(settings.BASE_DIR, settings.MASTER_DB_LOG_FILE)
BACKUP_FILE = os.path.join(settings.BASE_DIR, settings.BACKUP_LOG_FILE)


def parse_log_file():
    """
    Uses log-file for extracting applied changes on the stroer database.
    Extracted changes will be consumed by a celery periodic task for
    synchronizing JSONPlaceHolder database with stroer.
    After extracting changes, Log file will be cleared for the next iteration
    and all logs will be moved to a backup file for further use.
    """

    changes = {}

    with open(BACKUP_FILE, 'a+') as backup:
        with open(LOG_FILE, 'r+') as log_file:
            lines = [line.rstrip('\n') for line in log_file]
            for line in lines:
                log_entry = json.loads(line)

                instance_id = log_entry['instance_id']
                event = log_entry['event']
                model = log_entry['model']

                if model == "Post":
                    if instance_id not in changes:
                        changes[instance_id] = {
                            'action': None,
                            'model': model,
                            'update': None,
                        }

                    if event == ActionEnum.CREATE:
                        changes[instance_id]['action'] = ActionEnum.CREATE
                        changes[instance_id]['update'] = log_entry[
                            'instance_data']

                    elif event == ActionEnum.UPDATE:

                        if changes[instance_id]['action'] is not None:
                            changes[instance_id]['update'] = log_entry[
                                'instance_data'
                            ]
                        else:
                            changes[instance_id]['action'] = ActionEnum.UPDATE
                            changes[instance_id]['update'] = log_entry[
                                'instance_data'
                            ]

                    elif event == ActionEnum.DELETE:

                        if changes[instance_id]['action'] == ActionEnum.CREATE:
                            del changes[instance_id]

                        else:
                            changes[instance_id]['action'] = ActionEnum.DELETE
                            changes[instance_id]['update'] = log_entry[
                                'instance_data'
                            ]

                    backup.write(line + "\n")
                    log_file.truncate(0)

    return changes
