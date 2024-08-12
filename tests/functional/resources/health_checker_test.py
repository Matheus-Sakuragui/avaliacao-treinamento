from jsonschema import validate

from tests.functional.core.base_test import BaseTestCase
from tests.functional.resources.schemas.user_schema import \
    user_default_message_schema


class TestHealthCheckerResource(BaseTestCase):

    def test_server_is_up_and_running(self):
        response = self.client.get('/health')

        self.assert200(response)
        validate(instance=response.json, schema=user_default_message_schema)
        assert response.json['message'] == 'Service is up'
