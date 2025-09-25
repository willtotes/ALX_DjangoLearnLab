# API Filtering, Searching, and Ordering Documentation

## Overview
This API provides advanced query capabilities for filtering, searching, and ordering book and author data.

## Book Endpoints

### GET /api/books/
Retrieve books with advanced filtering capabilities.

#### Filtering Parameters:
- `publication_year` - Exact year match
- `publication_year__gte` - Years greater than or equal
- `publication_year__lte` - Years less than or equal
- `publication_year__gt` - Years greater than
- `publication_year__lt` - Years less than
- `publication_year_range` - Year range (e.g., `1990,2000`)
- `author_name` - Partial author name search
- `title` - Partial title search
- `title_exact` - Exact title match
- `search` - Search across title and author name

#### Search Parameters:
- `search` - Text search across title and author fields

#### Ordering Parameters:
- `ordering` - Sort results by field(s)
  - Examples: `title`, `-publication_year`, `author__name,title`

#### Examples: