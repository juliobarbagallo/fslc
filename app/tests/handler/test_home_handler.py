from http import HTTPStatus


class TestHomeHandler:
    @staticmethod
    def test_home_handler(test_client):
        response = test_client.get("/")
        assert response.status_code == HTTPStatus.OK
        assert b"Cuboids" in response.data
