from jsonschema import validate

from tests.functional.core.base_test import BaseTestCase
from tests.functional.resources.schemas.user_schema import (
    user_default_message_schema, user_default_response_schema)


class TestUserRegisterResource(BaseTestCase):

    def setUp(self):
        super().create_app()
        super().setUp()
        self.default_headers = {
            'Content-Type': 'application/json'
        }
        user_json = {
            "username": "user1",
            "password": "pwd1"
        }

        response = self.client.post('/token', json=user_json, headers=self.default_headers)
        if response.status_code == 201:
            self.access_token = response.json["access_token"]
            self.default_headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

    def test_add_new_user_with_success(self):
        new_user = {
            "username": "user999",
            "password": "pwd999"
        }
        response = self.client.post('/user', json=new_user)
        assert response.status_code == 201
        validate(instance=response.json, schema=user_default_response_schema)
        assert response.json['username'] == 'user999'

    def test_add_new_user_with_username_registered(self):
        new_user = {
            "username": "user1",
            "password": "pwd000"
        }
        response = self.client.post('/user', json=new_user)
        assert response.status_code == 400
        validate(instance=response.json, schema=user_default_message_schema)
        assert response.json['message'] == 'Username already exists'

    def test_update_user_with_success(self):
        update_user = {
            "username": "user77",
            "password": "pwd77"
        }
        response = self.client.put('/user?uid=3', json=update_user, headers=self.default_headers)
        assert response.status_code == 201
        validate(instance=response.json, schema=user_default_response_schema)
        assert response.json['id'] == 3
        assert response.json['username'] == 'user77'

    def test_update_nonexistent_user(self):
        update_user = {
            "username": "user77",
            "password": "pwd77"
        }
        response = self.client.put('/user?uid=999', json=update_user, headers=self.default_headers)
        assert response.status_code == 400
        validate(instance=response.json, schema=user_default_message_schema)
        assert response.json['message'] == 'User ID not exists'

    def test_get_user_by_id_api(self):
        response = self.client.get('/user?uid=1', headers=self.default_headers)
        assert response.status_code == 200
        validate(instance=response.json, schema=user_default_response_schema)
        assert response.json['username'] == 'user1'

    def test_get_nonexistent_user(self):
        response = self.client.get('/user?uid=999', headers=self.default_headers)
        assert response.status_code == 404
        validate(instance=response.json, schema=user_default_message_schema)
        assert response.json['message'] == 'User not found'

    def test_get_user_by_id_without_authtoken_api(self):
        response = self.client.get('/user?uid=1')
        assert response.status_code == 422

    def test_delete_user_with_success(self):
        response = self.client.delete('/user?uid=2', headers=self.default_headers)
        assert response.status_code == 201
        validate(instance=response.json, schema=user_default_message_schema)
        assert response.json['message'] == 'User deleted'

    def test_delete_nonexistent_user(self):
        response = self.client.delete('/user?uid=999', headers=self.default_headers)
        assert response.status_code == 404
        validate(instance=response.json, schema=user_default_message_schema)
        assert response.json['message'] == 'User not found'

    def tearDown(self):
        self.client.delete('/token', headers=self.default_headers)
