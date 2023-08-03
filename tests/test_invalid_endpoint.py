import pytest


@pytest.mark.usefixtures("test_setup", "test_teardown")
class TestInvalidEndpoint:
    def test_invalid_endpoint(self, test_setup):
        client, _, _ = test_setup

        response = client.get("/api/non_existing_endpoint")
        assert response.status_code == 404
