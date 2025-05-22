from fastapi.testclient import TestClient
from routers.user import app

client = TestClient(app)

def test_create_user():
    user_payload = {
        "name": "Bola Tinubu",
        "email": "bolatinubu@gmail.com"
    }
    response = client.post("/users/", json=user_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == user_payload["name"]
    assert response_data["email"] == user_payload["email"]

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= 2 

def test_get_user_found():
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id

def test_get_user_not_found():
    user_id = 100
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "User not found"

def test_update_user_found():
    user_id = 1
    update_payload = {
        "name": "Bola Tinubu",
        "email": "bolatinubu@gmail.com"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == update_payload["name"]
    assert response_data["email"] == update_payload["email"]

def test_update_user_not_found():
    user_id = 100
    update_payload = {
        "name": "Bola Tinubu",
        "email": "bolatinubu@gmail.com"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "User not found"

def test_delete_user_found():
    user_payload = {
        "name": "Bola Tinubu",
        "email": "bolatinubu@gmail.com"
    }
    response = client.post("/users/", json=user_payload)
    user_id = response.json()["id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "User deleted Successfully"

def test_delete_user_not_found():
    user_id = 100
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "User not found"


