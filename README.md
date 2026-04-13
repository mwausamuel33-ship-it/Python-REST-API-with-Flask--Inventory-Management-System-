# Inventory Management System - Python REST API

A simple yet comprehensive REST API for managing inventory items with external API integration. Built with Flask, this system allows employees to add, edit, view, and delete inventory items, and fetch real-time product data from the OpenFoodFacts API.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete inventory items
- **RESTful API**: Standard HTTP methods for resource management
- **External API Integration**: Fetch product data from OpenFoodFacts API by barcode or product name
- **CLI Interface**: Command-line tool to interact with the API
- **Error Handling**: Comprehensive error handling with meaningful error messages
- **Unit Tests**: Extensive test coverage using pytest
- **Mock Database**: In-memory data storage for quick prototyping

## Tech Stack

- **Framework**: Flask 2.3.3
- **HTTP Client**: Requests 2.31.0
- **Testing**: pytest 7.4.2, pytest-mock 3.11.1
- **Python Version**: 3.10+
- **Package Manager**: pip

## Code Refactoring (Junior Developer Edition)

This project has been refactored to be cleaner and more maintainable while keeping a junior developer style:

| File | Original | Refactored | Reduction |
|------|----------|-----------|-----------|
| **app.py** | 306 lines | 139 lines | 55% ↓ |
| **cli.py** | 425 lines | 119 lines | 72% ↓ |
| **Total** | 731 lines | 258 lines | 65% ↓ |

✨ **All functionality preserved** - Every feature works exactly as before!

**Key refactoring highlights:**
- Combined repetitive functions into reusable helpers
- Removed excessive comments and docstrings
- Simplified error handling logic
- Cleaner code structure without sacrificing readability
- Perfect for learning how to write efficient junior developer code

See [REFACTORING_SUMMARY.md](./REFACTORING_SUMMARY.md) for detailed changes.

## Project Structure

```
pythonRestAPI/
├── app.py              # Main Flask application with API endpoints
├── cli.py              # Command-line interface for API interaction
├── test_app.py         # Unit tests for all features
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── venv/               # Virtual environment (created during setup)
```

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step-by-Step Setup

1. **Clone or navigate to the repository**
   ```bash
   cd pythonRestAPI
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Flask Server

```bash
source venv/bin/activate
python app.py
```

The server will start on `http://localhost:5000`

Output:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Run the CLI Tool

In a new terminal:

```bash
source venv/bin/activate
python cli.py
```

This opens an interactive menu where you can:
1. View all inventory items
2. View single item by ID
3. Add new inventory item
4. Update inventory item
5. Delete inventory item
6. Search external API (OpenFoodFacts)
7. Exit

## API Endpoints

### Base URL: `http://localhost:5000`

### 1. Get All Inventory Items
- **Endpoint**: `GET /inventory`
- **Description**: Fetch all inventory items from the database
- **Response**: 
  ```json
  {
    "status": "success",
    "count": 2,
    "data": [
      {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "barcode": "5901234123457",
        "price": 3.99,
        "quantity": 45,
        "ingredients_text": "Filtered water, almonds, cane sugar...",
        "created_at": "2024-01-15"
      }
    ]
  }
  ```

### 2. Get Single Item by ID
- **Endpoint**: `GET /inventory/<id>`
- **Description**: Fetch a specific inventory item by ID
- **Example**: `GET /inventory/1`
- **Response**: 
  ```json
  {
    "status": "success",
    "data": {
      "id": 1,
      "product_name": "Organic Almond Milk",
      "brands": "Silk",
      "barcode": "5901234123457",
      "price": 3.99,
      "quantity": 45,
      "ingredients_text": "Filtered water, almonds, cane sugar...",
      "created_at": "2024-01-15"
    }
  }
  ```

### 3. Create New Item
- **Endpoint**: `POST /inventory`
- **Description**: Add a new inventory item
- **Request Body**:
  ```json
  {
    "product_name": "Greek Yogurt",
    "brands": "Fage",
    "price": 4.99,
    "quantity": 20,
    "barcode": "5901234123459",
    "ingredients_text": "Milk, cultures"
  }
  ```
- **Required Fields**: product_name, brands, price, quantity
- **Optional Fields**: barcode, ingredients_text
- **Response**: 201 Created
  ```json
  {
    "status": "success",
    "message": "Item created successfully",
    "data": {
      "id": 3,
      "product_name": "Greek Yogurt",
      ...
    }
  }
  ```

### 4. Update Item (PATCH)
- **Endpoint**: `PATCH /inventory/<id>`
- **Description**: Update an existing item (partial update supported)
- **Example**: `PATCH /inventory/1`
- **Request Body** (can include any of these fields):
  ```json
  {
    "price": 4.99,
    "quantity": 50,
    "product_name": "New Name",
    "brands": "New Brand"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "status": "success",
    "message": "Item updated successfully",
    "data": { ... }
  }
  ```

### 5. Delete Item
- **Endpoint**: `DELETE /inventory/<id>`
- **Description**: Remove an item from inventory
- **Example**: `DELETE /inventory/1`
- **Response**: 200 OK
  ```json
  {
    "status": "success",
    "message": "Item deleted successfully",
    "data": {
      "id": 1,
      ...
    }
  }
  ```

### 6. Search External API
- **Endpoint**: `POST /search-external`
- **Description**: Search OpenFoodFacts API for products by barcode or name
- **Request Body (by barcode)**:
  ```json
  {
    "barcode": "3017620425035"
  }
  ```
- **Request Body (by name)**:
  ```json
  {
    "product_name": "almond milk"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "status": "success",
    "data": {
      "product_name": "...",
      "brands": "...",
      "barcode": "...",
      "ingredients_text": "...",
      "quantity": "...",
      "image_url": "..."
    }
  }
  ```

## Example Usage

### Using cURL

```bash
# Get all items
curl http://localhost:5000/inventory

# Get single item
curl http://localhost:5000/inventory/1

# Create new item
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Greek Yogurt",
    "brands": "Fage",
    "price": 4.99,
    "quantity": 20
  }'

# Update item
curl -X PATCH http://localhost:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 5.99, "quantity": 60}'

# Delete item
curl -X DELETE http://localhost:5000/inventory/1

# Search external API
curl -X POST http://localhost:5000/search-external \
  -H "Content-Type: application/json" \
  -d '{"product_name": "milk"}'
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000"

# Create item
response = requests.post(
    f"{BASE_URL}/inventory",
    json={
        "product_name": "Greek Yogurt",
        "brands": "Fage",
        "price": 4.99,
        "quantity": 20
    }
)
print(response.json())

# Update item
response = requests.patch(
    f"{BASE_URL}/inventory/1",
    json={"price": 5.99}
)
print(response.json())
```

## Database Structure

The mock database stores items in a Python list with the following structure:

```python
{
    "id": 1,
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "barcode": "5901234123457",
    "price": 3.99,
    "quantity": 45,
    "ingredients_text": "Filtered water, almonds, cane sugar...",
    "created_at": "2024-01-15"
}
```

## Running Tests

### Run all tests
```bash
source venv/bin/activate
pytest test_app.py -v
```

### Run specific test
```bash
pytest test_app.py::test_get_all_inventory -v
```

### Run tests with coverage
```bash
pytest test_app.py --cov=. -v
```

### Test Coverage

The test suite includes:
- **GET Endpoint Tests**: Fetching all items and single items
- **POST Endpoint Tests**: Creating new items with validation
- **PATCH Endpoint Tests**: Updating items (full and partial)
- **DELETE Endpoint Tests**: Removing items
- **External API Tests**: Searching OpenFoodFacts API
- **Error Handler Tests**: 404, 405, 500 error scenarios
- **Integration Tests**: Complete CRUD workflow
- **Helper Function Tests**: ID generation logic

Currently there are **30+ unit tests** covering all major functionality.

## OpenFoodFacts API Integration

The system integrates with the free OpenFoodFacts API to fetch real product data:

- **Barcode Search**: `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`
- **Product Name Search**: `https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&json=1`

Note: Searches are rate-limited and may take 5-10 seconds.

## Error Handling

The API provides meaningful error responses:

```json
{
  "status": "error",
  "message": "Item with ID 999 not found"
}
```

Common error codes:
- **400**: Bad Request (missing required fields)
- **404**: Item Not Found
- **405**: Method Not Allowed
- **500**: Internal Server Error

## Git Workflow

This project uses Git for version control:

```bash
# Initialize repo
git init

# Create branches for features
git checkout -b feature/crud-endpoints
git checkout -b feature/external-api
git checkout -b feature/cli-interface
git checkout -b feature/unit-tests

# Make commits
git add .
git commit -m "Add CRUD endpoints for inventory"

# Merge branches
git checkout main
git merge feature/crud-endpoints
```

## Future Improvements

- [ ] Database persistence (SQLite, PostgreSQL)
- [ ] User authentication and authorization
- [ ] Advanced filtering and sorting
- [ ] Batch operations (bulk upload/delete)
- [ ] Caching for external API responses
- [ ] Rate limiting
- [ ] API documentation with Swagger
- [ ] Docker containerization
- [ ] Deployment to cloud platforms

## Troubleshooting

### Port 5000 already in use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Virtual environment not activating
```bash
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### OpenFoodFacts API timing out
- The API may be slow or unavailable
- Increase timeout in `app.py` or `cli.py`
- Try using a barcode instead of product name for faster results

## Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Write tests for new features
4. Submit a pull request

## License

This is an educational project created for learning purposes.

## Author

Created as a summative lab project for demonstrating:
- Flask REST API development
- CRUD operations
- External API integration
- CLI development
- Unit testing with pytest
- Git workflow and version control

## Contact & Support

For questions or issues, please check the code comments or refer to Flask and pytest documentation:
- Flask: https://flask.palletsprojects.com/
- pytest: https://docs.pytest.org/
- OpenFoodFacts API: https://world.openfoodfacts.org/api
