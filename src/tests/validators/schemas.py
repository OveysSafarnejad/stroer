def generate_list_schema_validator(object_schema):
    return {
        'count': {'type': 'integer', 'required': True},
        'next': {'type': 'string', "required": True, 'nullable': True},
        'previous': {'type': 'string', "required": True, 'nullable': True},
        'results': {
            'type': 'list',
            'schema':
                {
                    'type': 'dict',
                    'schema': object_schema
                }
        }
    }


post_schema = generate_list_schema_validator({
    'id': {'type': 'integer', "required": True},
    'title': {'type': 'string', "required": True},
    'body': {'type': 'string', "required": True},
    'user': {'type': 'dict', "required": True},
})

comment_schema = generate_list_schema_validator({
    'id': {'type': 'integer', "required": True},
    'api_comment_id': {'type': 'integer', "required": True, 'nullable': True},
    'post_id': {'type': 'integer', "required": True},
    'api_post_id': {'type': 'integer', "required": True, 'nullable': True},
    'name': {'type': 'string', "required": True},
    'email': {'type': 'string', "required": True},
    'body': {'type': 'string', "required": True},
})
