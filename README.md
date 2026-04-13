# Inventory System

This is a Flask app for inventory. You can add, view, update, delete items. Also gets data from external API.

## Setup

1. Install Flask: pip install flask requests
2. Run app: python app.py

## How to use

Start server then use browser or curl.

Endpoints:
- GET /inventory - get all items
- GET /inventory/<id> - get one item
- POST /inventory - add item (send json with name, brand, price, qty)
- PATCH /inventory/<id> - update item
- DELETE /inventory/<id> - delete item
- POST /search-external - search API by barcode or name

## Tests

Run: pytest test_app.py