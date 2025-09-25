# Advanced API Project - Custom Views Documentation

## Overview
This project demonstrates advanced Django REST Framework usage with custom generic views, permissions, and API endpoints for Book and Author management.

## View Configurations

### Book Views

#### 1. BookListView (`/api/books/`)
- **Purpose**: Retrieve all books with filtering and searching
- **Methods**: GET
- **Permissions**: AllowAny (public access)
- **Features**:
  - Filter by `publication_year` and `author__id`
  - Search by `title` and `author__name`
  - Order by multiple fields
  - Pagination support

#### 2. BookCreateView (`/api/books/create/`)
- **Purpose**: Create new book instances
- **Methods**: POST
- **Permissions**: IsAuthenticated
- **Custom Hooks**:
  - `perform_create()`: Extend creation logic
  - Custom response format with success message

#### 3. BookDetailView (`/api/books/<id>/`)
- **Purpose**: Retrieve single book details
- **Methods**: GET
- **Permissions**: AllowAny

#### 4. BookUpdateView (`/api/books/<id>/update/`)
- **Purpose**: Modify existing books
- **Methods**: PUT, PATCH
- **Permissions**: IsAuthenticated

#### 5. BookDeleteView (`/api/books/<id>/delete/`)
- **Purpose**: Remove books
- **Methods**: DELETE
- **Permissions**: IsAuthenticated
- **Customization**: Enhanced delete confirmation response

### Combined Views

#### BookListCreateView (`/api/books-combined/`)
- **Purpose**: Combined list and create operations
- **Methods**: GET, POST
- **Permissions**: Dynamic (public read, authenticated write)
- **Advanced Features**:
  - Custom queryset filtering
  - Range filtering by publication year

#### BookRetrieveUpdateDestroyView (`/api/books-combined/<id>/`)
- **Purpose**: Complete CRUD operations for individual books
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: Dynamic based on HTTP method

## Permission System

### Built-in Permissions Used:
- `AllowAny`: Public access
- `IsAuthenticated`: Requires login
- `IsAuthenticatedOrReadOnly`: Public read, authenticated write

### Custom Permissions:
- `IsAuthenticatedOrReadOnly`: Enhanced version with extensibility
- `IsOwnerOrReadOnly`: Object-level permissions (for future use)

## Testing the API

### Manual Testing with curl:

```bash
# List all books (public)
curl http://localhost:8000/api/books/

# Get specific book (public)
curl http://localhost:8000/api/books/1/

# Create book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{"title": "New Book", "publication_year": 2023, "author": 1}'

# Update book (requires authentication)
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{"title": "Updated Title", "publication_year": 2023, "author": 1}'