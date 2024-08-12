from jsonschema import validate

from tests.functional.core.base_test import BaseTestCase
from tests.functional.resources.schemas.user_schema import \
    user_default_message_schema


class TestTokenResource(BaseTestCase):

    def setUp(self):
        super().create_app()
        super().setUp()
        self.default_headers = {
            'Content-Type': 'application/json'
        }

    def test_login_invalid_credentials(self):
        invalid_user_credentials = {
            "username": "user999",
            "password": "pwd999"
        }

        response = self.client.post('/token', json=invalid_user_credentials, headers=self.default_headers)
        assert response.status_code == 401
        validate(instance=response.json, schema=user_default_message_schema)
        assert response.json['message'] == 'Invalid username or password'

    def tearDown(self):
        self.client.delete('/token', headers=self.default_headers)
