import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/"
AUTH_URL = BASE_URL + "auth-token/"
REGISTER_URL = BASE_URL + "register/"
BOOKS_URL = BASE_URL + "books_all/"

def test_authentication():
    print("Testing Authentication and Permissions")
    print("=" * 50)
    
    print("\n1. Testing unauthenticated list access:")
    response = requests.get(BOOKS_URL)
    print(f"Status: {response.status_code}")
    
    print("\n2. Testing unauthenticated create (should fail):")
    response = requests.post(BOOKS_URL, json={
        "title": "Unauthorized Book",
        "author": "Unauthorized Author"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    print("\n3. Registering new user:")
    response = requests.post(REGISTER_URL, json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("User registered successfully")
    
    print("\n4. Getting auth token:")
    response = requests.post(AUTH_URL, json={
        "username": "testuser",
        "password": "testpassword123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token = response.json()['token']
        print(f"Token: {token}")
        
        print("\n5. Testing authenticated create:")
        headers = {'Authorization': f'Token {token}'}
        response = requests.post(BOOKS_URL, json={
            "title": "Authenticated Book",
            "author": "Authenticated Author"
        }, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            book_id = response.json()['id']
            print(f"Created book ID: {book_id}")
            
            print(f"\n6. Testing authenticated delete for book {book_id}:")
            response = requests.delete(f"{BOOKS_URL}{book_id}/", headers=headers)
            print(f"Status: {response.status_code}")

if __name__ == "__main__":
    test_authentication()