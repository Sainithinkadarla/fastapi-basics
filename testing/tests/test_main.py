from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["Message"] == "Welcome to api"

def test_create_item():
    response = client.post("/items", params={"name": "apple", "description": "but not apple"})
    assert response.status_code == 200
    assert response.json()["name"] == "apple"

def test_get_item():
    create_response = client.post("/items", params={"name": "dog", "description": "but not dog"})
    item_id = create_response.json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.json()['id'] == item_id
    assert response.status_code == 200

def test_read_non_existent_item():
    response = client.get("/items/123123123")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"