# Inventory Management API

A simple Inventory Management API built with FastAPI.

## Features

- View all inventory items
- View single item
- Add new item
- Update item
- Delete item
- Filter items by category
- Find low stock items
- Restock inventory
- Sell inventory

## Tech Stack

- FastAPI
- Python
- Pydantic

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/inventory-management-api.git
cd inventory-management-api
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Example Item

```json
{
  "id": 1,
  "name": "Laptop",
  "category": "Electronics",
  "quantity": 10,
  "price": 3500
}
```

## Endpoints

### Get All Items

```http
GET /items
```

### Get Item By ID

```http
GET /items/{id}
```

### Create Item

```http
POST /items
```

### Update Item

```http
PUT /items/{id}
```

### Delete Item

```http
DELETE /items/{id}
```

### Restock Item

```http
POST /items/{id}/restock
```

### Sell Item

```http
POST /items/{id}/sell
```

## Future Improvements

- SQLite Database
- PostgreSQL
- User Authentication
- JWT Tokens
- Pagination
- Search and Sorting
- Supplier Management

## Author

Shamshad