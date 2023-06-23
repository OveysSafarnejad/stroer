from cerberus import Validator
from rest_framework.test import APITestCase


def generate_list_schema_validator(object_schema):
    return {
        'count': {'type': 'integer', 'required': True},
        'next': {'type': 'string', "required": True, 'nullable': True},
        'previous': {'type': 'string', "required": True, 'nullable': True},
        'results': {'type': 'list',
                    'schema': {'type': 'dict', 'schema': object_schema}}
    }


class BaseAPITestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def check_response_schema(self, schema, response):
        validator = Validator(schema)
        is_valid = validator.validate(response)
        if not is_valid:
            print(f'Validator Error:{validator.errors}')
        self.assert_(validator.validate(response))

    def tearDown(self) -> None:
        super(BaseAPITestCase, self).tearDown()
