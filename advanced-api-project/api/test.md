# API Tests Documentation

## Overview
This test suite validates the functionality of the advanced_api_project API endpoints, including CRUD operations, filtering, searching, ordering, and authentication.

## Test Structure

### Test Classes:
- `BookCRUDTests`: Tests Create, Read, Update, Delete operations for books
- `BookFilteringTests`: Tests filtering, searching, and ordering capabilities
- `BookValidationTests`: Tests validation rules and error handling
- `AuthorCRUDTests`: Tests CRUD operations for authors
- `PaginationTests`: Tests pagination functionality
- `ErrorHandlingTests`: Tests edge cases and error scenarios

## Running Tests

### Run All Tests:
```bash
python manage.py test api.test_views