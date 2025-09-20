import requests
import json

BASE_URL =  "http://127.0.0.1:8000/api/books_all/"

def test_crud_operations():
    print("Testing CRUD operations.")

    print("\n1. Creating a New Book!")
    new_book = {
        'title': 'Test Book',
        'author': 'Test Author'
    }
    response = requests.post(BASE_URL, json=new_book)
    print(f"POST Response: {response.status_code}")
    print(f"Created Book: {response.json()}")

    book_id = response.json()['id']

    print(f"\n2. Retrieving book {book_id}...")
    response = requests.get(f"{BASE_URL}{book_id}/")
    print(f"GET Response: {response.status_code}")
    print(f"Book Details: {response.json()}")

    print(f"\n3. Updating book {book_id}...")
    updated_book = {
        'title': 'Updated Test Book',
        'author': 'Updated Test Author'
    }
    response = requests.put(f"{BASE_URL}{book_id}/", json=updated_book)
    print(f"PUT Response: {response.status_code}")
    print(f"Updated Book: {response.json()}")

    print(f"\n4. Listing all books!")
    response = requests.get(BASE_URL)
    print(f"GET All Response: {response.status_code}")
    print(f"Total Books: {len(response.json())}")

    print(f"\n5. Deleting book {book_id}!")
    response = requests.delete(f"{BASE_URL}{book_id}/")
    print(f"DELETE Response: {response.status_code}")

    print(f"\n6 Verifying book {book_id} is deleted!!!")
    response = requests.get(f"{BASE_URL}{book_id}/")
    print(f"GET Deleted Book Response: {response.status_code}")

if __name__ == "__main__":
    test_crud_operations()
    

