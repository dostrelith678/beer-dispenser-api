import pytest
import json


@pytest.mark.usefixtures("test_setup", "test_teardown")
class TestAuth:
    def test_login_with_valid_credentials(self, test_setup):
        client, _, _ = test_setup

        data = {"username": "test_user", "password": "test_password"}
        response = client.post(
            "/auth/login", data=json.dumps(data), content_type="application/json"
        )
        data = response.get_json()

        assert response.status_code == 200
        assert "access_token" in data

    def test_login_with_invalid_credentials(self, test_setup):
        client, _, _ = test_setup

        data = {"username": "test_user", "password": "wrong_password"}
        response = client.post(
            "/auth/login", data=json.dumps(data), content_type="application/json"
        )
        data = response.get_json()

        assert response.status_code == 401
