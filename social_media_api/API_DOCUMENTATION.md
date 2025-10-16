# Social Media API - Posts and Comments Documentation

## Posts Endpoints

### List Posts
**GET** `/api/posts/`

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Number of posts per page (default: 10, max: 100)
- `search` - Search in title, content, and author username
- `author` - Filter by author username
- `liked` - Filter posts liked by current user (true/false)
- `ordering` - Order by: created_at, -created_at, likes_count, etc.

**Response:**
```json
{
    "links": {
        "next": null,
        "previous": null
    },
    "count": 1,
    "page_size": 10,
    "total_pages": 1,
    "current_page": 1,
    "results": [
        {
            "id": 1,
            "author": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "bio": "This is my bio",
                "profile_picture": null,
                "followers_count": 0,
                "following_count": 0,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            },
            "title": "My First Post",
            "content": "This is the content of my first post",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "likes_count": 5,
            "comments_count": 3,
            "is_liked": true,
            "comments": []
        }
    ]
}

# Social Media API - Follow System and Feed Documentation

## Follow Management Endpoints

### Follow a User
**POST** `/api/auth/follow/`

**Headers:**