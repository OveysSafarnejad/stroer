added_change_result = {
    795: {
        'action': 0,
        'model': 'Post',
        'update': {
            'api_post_id': None,
            'body': 'Hallo!',
            'created_time': '',
            'creator_id': None,
            'id': 795,
            'modified_time': '',
            'modifier_id': None,
            'title': 'post2',
            'user_id': 99999942
        }
    }
}

added_deleted_result = {}

added_updated_result = {
    795: {
        'action': 0,
        'model': 'Post',
        'update': {
            'body': 'NEW BODY',
            'creator_id': None,
            'id': 795,
            'modifier_id': None,
            'title': 'UPDATED',
            'user_id': 1
        }
    }
}

deleted_result = {
    794: {
        'action': 2,
        'model': 'Post',
        'update': {
            'body': 'Hallo!', 'id': 794, 'title': 'post2', 'user_id': 1
        }
    }
}
updated_result = {
    792: {
        'action': 1,
        'model': 'Post',
        'update': {
            'body': 'NEW BODY2',
            'creator_id': None,
            'id': 792,
            'modifier_id': None,
            'title': 'UPDATED2',
            'user_id': 1
        }
    }
}
updated_deleted_result = {
    796: {
        'action': 2,
        'model': 'Post',
        'update': {
            'body': 'NEW BODY',
            'id': 796,
            'title': 'UPDATED',
            'user_id': 1
        }
    }
}
