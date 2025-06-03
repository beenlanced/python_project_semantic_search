from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)

# Test Endpoint 1
url1 = "http://127.0.0.1:8000/"

def test_default_endpoint() -> None:
    """ 
    GIVEN a FASTAPI application configured for testing
    WHEN the '/' endpoint is requested (GET)
    THEN check for 200 status return code and that "health_check` message was received as "ok"
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "OK"}

def test_info_endpoint() -> None:
    """ 
    GIVEN a FASTAPI application configured for testing
    WHEN the '/info' endpoint is requested (GET)
    THEN check for 200 status return code and that
        {"name": "YouTube-Search", "description": "Search API for Shaw Talebi's YouTube videos."}
        was received
    """
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {"name": "YouTube-Search", "description": "Search API for Shaw Talebi's YouTube videos."}

def test_search_endpoint() -> None:
    """ 
    GIVEN a FASTAPI application configured for testing and
        a query = "text embeddings simply explained" 
    WHEN the '/search/{query}' endpoint is requested (GET)
    THEN check for 200 status return code and that 
        a list of video titles of type str are provided
    """
    query = "text embeddings simply explained"
    params = {"query": query}
    response = client.get("/search", params=params)
    assert response.status_code == 200
    assert response.json() is not None