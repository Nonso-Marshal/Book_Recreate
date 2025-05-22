from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


def test_update_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    update_payload = {
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "year": 1956,
        "pages": 600,
        "language": "Nigerian English"
    }
    update_response = client.put(f"/books/{book_id}", json=update_payload)
    update_book_data = update_response.json()
    assert update_response.status_code == 200
    assert update_book_data['message'] == "Book updated successfully"
    assert update_book_data['data']['title'] == update_payload['title']

def test_update_book_not_found():
    book_id = str(uuid4())
    update_payload = {
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "year": 1956,
        "pages": 600,
        "language": "Nigerian English"
    }
    update_response = client.put(f"/books/{book_id}", json=update_payload)
    assert update_response.status_code == 404
    assert update_response.json()["detail"] == f"Book with id: {book_id} not found"



def test_delete_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    delete_response = client.delete(f"/books/{book_id}")
    delete_book_data = delete_response.json()
    assert delete_response.status_code == 200
    assert delete_book_data['message'] == "Book deleted successfully"
