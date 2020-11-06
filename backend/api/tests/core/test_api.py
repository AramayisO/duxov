from starlette import status
from starlette.testclient import TestClient

from app.main import app


def test_doc_route_available(client: TestClient):
    """
    Test that the rest api docs route is available.
    """
    response = client.get(app.url_path_for('get_api_docs'))

    assert response.status_code == status.HTTP_200_OK
