# Inventory Management System

A Flask REST API for managing inventory items. You can add, view, update, and delete items. Also integrates with OpenFoodFacts API to search for real product data.

## What This Does

- Create, read, update, and delete inventory items (CRUD)
- Search for products using the OpenFoodFacts API by barcode or product name
- Command-line interface to manage inventory
- REST API with proper HTTP methods
- Unit tests to validate all functionality

## Technologies Used

- Python 3.8+
- Flask 2.3.3 (web framework)
- Requests 2.31.0 (HTTP library)
- pytest 7.4.2 (testing)

## Project Files

```
pythonRestAPI/
├── app.py              # Flask API server
├── cli.py              # Command-line interface
├── test_app.py         # Unit tests
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## Installation

### Requirements
- Python 3.8 or higher
- pip

### Setup

1. Go to the project folder
```bash
cd pythonRestAPI
```

2. Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## How to Run

### Start the API Server

```bash
python app.py
```

The server will run on `http://localhost:5000`

### Start the CLI

Open a new terminal (keep the API running) and run:
```bash
python cli.py
```

Follow the menu to add, view, update, or delete items.

## API Endpoints

All endpoints are at `http://localhost:5000`

### Get Items
- `GET /inventory` - Get all items
- `GET /inventory/<id>` - Get one item by ID

### Create Item
- `POST /inventory` - Add a new item

Requires: `product_name`, `brands`, `price`, `quantity`

Example:
```bash
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Milk","brands":"Local","price":2.99,"quantity":10}'
```

### Update Item
- `PATCH /inventory/<id>` - Update an item

Example:
```bash
curl -X PATCH http://localhost:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price":3.50}'
```

### Delete Item
- `DELETE /inventory/<id>` - Delete an item

### Search External API
- `POST /search-external` - Search OpenFoodFacts for products

You can search by barcode or product name.

## Using the CLI

The menu has these options:

1. **View All Items** - See all products in inventory
2. **View Single Item** - Look up one item by ID
3. **Add New Item** - Create a new product
4. **Update Item** - Change product info
5. **Delete Item** - Remove a product
6. **Search External API** - Find products from OpenFoodFacts
7. **Exit** - Close the program

Example of adding an item:
```
Enter your choice (1-7): 3

============================================================
  ADD NEW ITEM
============================================================

  Product Name: Orange Juice
  Brand: Tropicana
  Barcode (optional): 
  Price ($): 3.49
  Quantity: 15
  Ingredients (optional): 

✓ SUCCESS: Item added successfully (ID: 3)
```

## Running Tests

Run all tests:
```bash
pytest test_app.py -v
```

Run one specific test:
```bash
pytest test_app.py::test_get_all_inventory -v
```

## What Gets Tested

The test file has tests for:
- Getting all items and single items
- Creating items with validation
- Updating items (full and partial updates)
- Deleting items
- Searching external API
- Error cases (item not found, bad requests, etc.)
- Helper functions

Total: 17+ tests

## Data Format

Items stored look like this:

```json
{
  "id": 1,
  "product_name": "Almond Milk",
  "brands": "Silk",
  "barcode": "123456789",
  "price": 3.99,
  "quantity": 20,
  "ingredients_text": "water, almonds, sugar",
  "created_at": "2024-01-15"
}
```

## Errors

The API returns different HTTP codes:
- `200` - Success
- `201` - Item created
- `400` - Bad request (missing fields)
- `404` - Item not found
- `405` - Wrong HTTP method
- `500` - Server error

## External API

Uses the free OpenFoodFacts API to search for real products:
- Search by barcode (faster)
- Search by product name

Barcode search is usually faster than product name search.

## Troubleshooting

**Port 5000 already in use?**
Change the port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Connection refused?**
Make sure the Flask server is running before starting the CLI.

**Tests failing?**
Make sure the Flask server is NOT running when you run tests.

**Virtual environment not working?**
Windows: `venv\Scripts\activate`
Mac/Linux: `source venv/bin/activate`

**OpenFoodFacts API slow?**
Try searching by barcode instead of product name. The API might also be slow.

## Quick Start

```bash
# Terminal 1
python app.py

# Terminal 2 (new terminal)
python cli.py
```

Or to test with curl:
```bash
# Get all items
curl http://localhost:5000/inventory

# Get one item
curl http://localhost:5000/inventory/1

# Search for products
curl -X POST http://localhost:5000/search-external \
  -H "Content-Type: application/json" \
  -d '{"product_name":"milk"}'
```

## Notes

- This is a learning project for Flask and REST APIs
- Data is stored in memory - it resets when you restart the server
- Use a real database (SQLite, PostgreSQL) for production
- This was made for a lab assignment

## What I Learned

Building this project taught me about:
- Flask routing and REST API design
- CRUD operations
- Working with external APIs
- Building a CLI interface
- Unit testing with pytest
- Request validation and error handling
- Working with JSON

## Future Ideas

Things that could be added:
- Real database (SQLite or PostgreSQL)
- User login/authentication
- Search and filtering features
- Batch operations
- API documentation (Swagger)
- Web interface

---

Made as a summative lab project for Python Flask development.
