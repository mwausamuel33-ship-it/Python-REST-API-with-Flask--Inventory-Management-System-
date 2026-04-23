# Inventory Management System - Flask REST API

A Flask REST API for managing inventory items with external API integration to fetch product information from OpenFoodFacts.

## Features

- **CRUD Operations**: Create, Read, Update, Delete inventory items
- **RESTful API**: Built with Flask using standard HTTP methods
- **External API Integration**: Search products from OpenFoodFacts API
- **CLI Interface**: Command-line tool to interact with the API
- **Unit Tests**: Comprehensive test coverage using pytest
- **Input Validation**: Validates user input and API responses

## Tech Stack

- Python 3.8+
- Flask 2.3.3
- Requests 2.31.0
- pytest 7.4.2
- Virtual Environment

## Project Structure

```
pythonRestAPI/
├── app.py              # Flask API server
├── cli.py              # Command-line interface
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone or navigate to repository
```bash
cd pythonRestAPI
```

2. Create virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the API Server

Open terminal and run:
```bash
python app.py
```

Server will start on `http://localhost:5000`

### Run the CLI Tool

In a **new terminal** (with virtual environment activated):
```bash
python cli.py
```

Follow the menu prompts to manage inventory.

## API Endpoints

### Base URL: `http://localhost:5000`

**CRUD Operations:**
- `GET /inventory` - Get all items
- `GET /inventory/<id>` - Get single item by ID
- `POST /inventory` - Create new item
- `PATCH /inventory/<id>` - Update item
- `DELETE /inventory/<id>` - Delete item

**External API:**
- `POST /search-external` - Search OpenFoodFacts API

### Create Item Example

```bash
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Almond Milk",
    "brands": "Silk",
    "price": 3.99,
    "quantity": 20
  }'
```

### Update Item Example

```bash
curl -X PATCH http://localhost:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.99, "quantity": 15}'
```

## CLI Features

Menu Options:
1. **View All Items** - Display all inventory items with details
2. **View Single Item** - Look up item by ID
3. **Add New Item** - Create new product with validation
4. **Update Item** - Modify existing items
5. **Delete Item** - Remove items with confirmation
6. **Search External API** - Find products by barcode or name
7. **Exit** - Close application

### Add Item Example

```
Enter your choice (1-7): 3

============================================================
  ADD NEW ITEM
============================================================

  Product Name: Greek Yogurt
  Brand: Fage
  Barcode (optional): 5901234123459
  Price ($): 4.99
  Quantity: 20
  Ingredients (optional): Milk, cultures

✓ SUCCESS: Item added successfully (ID: 3)
```

## Running Tests

Run all tests:
```bash
pytest test_app.py -v
```

Run specific test:
```bash
pytest test_app.py::test_get_all_inventory -v
```

## Test Coverage

The test suite includes tests for:
- **GET endpoints** - Retrieving items
- **POST endpoints** - Creating items with validation
- **PATCH endpoints** - Updating items (full and partial)
- **DELETE endpoints** - Removing items
- **External API** - OpenFoodFacts search functionality
- **Helper functions** - ID generation and item lookup
- **Error handlers** - 404, 405, 500 errors

Total: **17+ unit tests**

## Database Structure

Items are stored in memory with the following structure:

```json
{
  "id": 1,
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "barcode": "5901234123457",
  "price": 3.99,
  "quantity": 45,
  "ingredients_text": "Filtered water, almonds, cane sugar",
  "created_at": "2024-01-15"
}
```

**Fields:**
- `id` - Auto-generated unique identifier
- `product_name` - Name of product (required)
- `brands` - Brand/manufacturer (required)
- `price` - Price in dollars (required)
- `quantity` - Stock quantity (required)
- `barcode` - Product barcode (optional)
- `ingredients_text` - Ingredient info (optional)
- `created_at` - Creation date (auto)

## Error Handling

The API returns proper HTTP status codes:
- `200` - Success (GET, PATCH, DELETE)
- `201` - Item created (POST)
- `400` - Bad Request (missing required fields)
- `404` - Item not found
- `405` - Method not allowed
- `500` - Server error

Error responses follow this format:
```json
{
  "status": "error",
  "message": "Item with ID 999 not found"
}
```

## External API Integration

The system uses the free OpenFoodFacts API:
- **Barcode Search:** `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`
- **Product Search:** `https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&json=1`

Search by barcode for faster results. The API may take 5-10 seconds for product name searches.

## Troubleshooting

### Port 5000 Already in Use
Change the port in `app.py` line 419:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Connection Refused Error
Make sure the Flask server is running in another terminal before starting CLI.

### Tests Failing
Ensure Flask server is **NOT** running when running tests.

### Virtual Environment Issues

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### OpenFoodFacts Timeout
The external API may be slow. Try:
- Search by barcode instead of product name
- Increase timeout in code (currently 5-10 seconds)
- Check if API is available at https://world.openfoodfacts.org/

## How It Works

### API Flow
1. Client sends HTTP request to Flask server
2. Flask route handler processes request
3. Data is validated
4. Operations are performed on mock database (inventory list)
5. JSON response is returned to client

### CLI Flow
1. User selects menu option
2. CLI prompts for required information
3. Input is validated
4. HTTP request is sent to API
5. Response is displayed in formatted output

### External API Flow
1. User searches for product by barcode or name
2. Request is sent to OpenFoodFacts API
3. Product data is retrieved
4. Data is formatted and displayed
5. User can optionally add product to inventory

## Future Improvements

Possible enhancements:
- [ ] Database persistence (SQLite, PostgreSQL)
- [ ] User authentication
- [ ] Advanced filtering and sorting
- [ ] Batch operations
- [ ] Caching for API responses
- [ ] Swagger API documentation
- [ ] Docker containerization
- [ ] Web interface (frontend)

## Running the Project

Quick start:
```bash
# Terminal 1 - Start API
python app.py

# Terminal 2 - Run CLI (in new terminal)
python cli.py

# Terminal 3 - Run tests (kill other terminals first)
pytest test_app.py -v
```

## Testing the API with cURL

Get all items:
```bash
curl http://localhost:5000/inventory
```

Get single item:
```bash
curl http://localhost:5000/inventory/1
```

Search external API:
```bash
curl -X POST http://localhost:5000/search-external \
  -H "Content-Type: application/json" \
  -d '{"product_name": "milk"}'
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [OpenFoodFacts API](https://world.openfoodfacts.org/api)
- [Requests Library](https://requests.readthedocs.io/)

## Notes

- This is a learning project for Flask and REST API development
- Data is stored in memory and resets when server restarts
- External API calls may be slow depending on network and API availability
- For production use, implement a real database like PostgreSQL

---

