# Permission and Group System Documentation

## Overview
This Django application implements a comprehensive permission system using custom permissions and user groups to control access to various parts of the application.

## Groups and Their Permissions

### 1. Viewers Group
- **Permissions**: `can_view_book`, `can_view_author`
- **Access**: Read-only access to view books and authors
- **Use Case**: Regular users who can browse but not modify content

### 2. Editors Group
- **Permissions**: `can_view_book`, `can_create_book`, `can_edit_book`, `can_view_author`, `can_create_author`, `can_edit_author`
- **Access**: Can view, create, and edit books and authors
- **Use Case**: Content managers who can manage library content

### 3. Admins Group
- **Permissions**: All permissions (view, create, edit, delete for both books and authors)
- **Access**: Full administrative access
- **Use Case**: System administrators with complete control

## Setup Instructions

1. **Run migrations**: `python manage.py makemigrations` then `python manage.py migrate`
2. **Create groups**: `python manage.py setup_groups`
3. **Assign users to groups** through Django admin interface

## Testing Permissions

### Test Users Setup:
1. Create test users in Django admin
2. Assign users to different groups:
   - User A → Viewers group
   - User B → Editors group
   - User C → Admins group

### Expected Behavior:
- **Viewers**: Can only view books/authors, cannot create/edit/delete
- **Editors**: Can view, create, and edit books/authors, cannot delete
- **Admins**: Full access to all operations

## Custom Permissions
The system uses these custom permissions:
- `can_view_*` - View object details
- `can_create_*` - Create new objects
- `can_edit_*` - Edit existing objects
- `can_delete_*` - Delete objects

## View Protection
Views are protected using Django's `@permission_required` decorator:
```python
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):