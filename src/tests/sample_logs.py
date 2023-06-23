added = '''{"event": 0, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "created_time": "", "modified_time": "", "creator_id": null, "modifier_id": null, "api_post_id": null, "title": "post2", "body": "Hallo!", "user_id": 99999942}}'''

added_deleted = '''{"event": 0, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "created_time": "2023-06-20 13:23:30.360106+00:00", "modified_time": "2023-06-20 13:23:30.360147+00:00", "creator_id": null, "modifier_id": null, "api_post_id": null, "title": "post2", "body": "Hallo!", "user_id": 99999942}}
{"event": 1, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "title": "UPDATED", "body": "NEW BODY", "user_id": 1, "modifier_id": null, "creator_id": null}}
{"event": 2, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "title": "UPDATED", "body": "NEW BODY", "user_id": 1}}'''

added_updated = '''{"event": 0, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "created_time": "", "modified_time": "", "creator_id": null, "modifier_id": null, "api_post_id": null, "title": "post2", "body": "Hallo!", "user_id": 99999942}}
{"event": 1, "model": "Post", "instance_id": 795, "instance_data": {"id": 795, "title": "UPDATED", "body": "NEW BODY", "user_id": 1, "modifier_id": null, "creator_id": null}}'''

deleted = '''{"event": 2, "model": "Post", "instance_id": 794, "instance_data": {"id": 794, "title": "post2", "body": "Hallo!", "user_id": 1}}'''

updated = '''{"event": 1, "model": "Post", "instance_id": 792, "instance_data": {"id": 792, "title": "UPDATED", "body": "NEW BODY", "user_id": 1, "modifier_id": null, "creator_id": null}}
{"event": 1, "model": "Post", "instance_id": 792, "instance_data": {"id": 792, "title": "UPDATED2", "body": "NEW BODY2", "user_id": 1, "modifier_id": null, "creator_id": null}}'''

updated_deleted = '''{"event": 1, "model": "Post", "instance_id": 796, "instance_data": {"id": 796, "title": "UPDATED", "body": "NEW BODY", "user_id": 1, "modifier_id": null, "creator_id": null}}
{"event": 2, "model": "Post", "instance_id": 796, "instance_data": {"id": 796, "title": "UPDATED", "body": "NEW BODY", "user_id": 1}}'''
