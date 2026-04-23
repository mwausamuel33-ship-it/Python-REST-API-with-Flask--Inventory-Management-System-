"""
Inventory Management System - Flask REST API
This Flask application provides a REST API for managing inventory items
and integrating with the OpenFoodFacts API to fetch product information.
"""

from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Mock database - stores inventory items in memory
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "barcode": "5901234123457",
        "price": 3.99,
        "quantity": 45,
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "created_at": "2024-01-15"
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brands": "Nature's Best",
        "barcode": "5901234123458",
        "price": 2.49,
        "quantity": 30,
        "ingredients_text": "Whole wheat flour, water, yeast, salt",
        "created_at": "2024-01-20"
    }
]


def get_next_id():
    """
    Generate the next available ID for a new inventory item.
    Gets the maximum ID from existing items and adds 1.
    Returns 1 if inventory is empty.
    """
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


def find_item(item_id):
    """
    Search for an item in inventory by its ID.
    
    Args:
        item_id (int): The ID of the item to find
        
    Returns:
        dict: The item if found, None otherwise
    """
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


# ============= ROUTES =============

@app.route('/', methods=['GET'])
def home():
    """Welcome endpoint - returns API status"""
    return jsonify({
        "status": "success",
        "message": "Welcome to Inventory Management API"
    }), 200


@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    """
    GET /inventory - Retrieve all inventory items
    Returns: JSON with status, count of items, and list of all items
    """
    return jsonify({
        "status": "success",
        "count": len(inventory),
        "data": inventory
    }), 200


@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    """
    GET /inventory/<id> - Retrieve a single inventory item by ID
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        JSON with status and item data (200 if found, 404 if not found)
    """
    item = find_item(item_id)
    
    if item:
        return jsonify({
            "status": "success",
            "data": item
        }), 200
    
    return jsonify({
        "status": "error",
        "message": f"Item with ID {item_id} not found"
    }), 404


@app.route('/inventory', methods=['POST'])
def create_inventory_item():
    """
    POST /inventory - Create a new inventory item
    
    Required JSON fields:
        - product_name (string): Name of the product
        - brands (string): Brand of the product
        - price (float): Price of the product
        - quantity (int): Quantity in stock
        
    Optional JSON fields:
        - barcode (string): Product barcode
        - ingredients_text (string): Ingredient information
        
    Returns:
        JSON with status and created item data (201 if successful, 400 if validation fails)
    """
    request_data = request.get_json()
    
    # List of required fields
    required_fields = ["product_name", "brands", "price", "quantity"]
    
    # Validate request has data and all required fields
    if not request_data or not all(field in request_data for field in required_fields):
        return jsonify({
            "status": "error",
            "message": "Missing required fields: product_name, brands, price, quantity"
        }), 400
    
    # Create new item with provided data
    new_item = {
        "id": get_next_id(),
        "product_name": request_data["product_name"],
        "brands": request_data["brands"],
        "barcode": request_data.get("barcode", ""),
        "price": float(request_data["price"]),
        "quantity": int(request_data["quantity"]),
        "ingredients_text": request_data.get("ingredients_text", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Add to inventory
    inventory.append(new_item)
    
    return jsonify({
        "status": "success",
        "message": "Item created successfully",
        "data": new_item
    }), 201


@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    """
    PATCH /inventory/<id> - Update an existing inventory item
    Supports partial updates - only include fields you want to update
    
    Accepted fields:
        - product_name, brands, barcode, ingredients_text (string)
        - price (float), quantity (int)
        
    Returns:
        JSON with status and updated item data (200 if successful, 404 if item not found)
    """
    # Find the item
    item = find_item(item_id)
    
    if not item:
        return jsonify({
            "status": "error",
            "message": f"Item with ID {item_id} not found"
        }), 404
    
    request_data = request.get_json()
    
    # Update each field if it exists in the request
    if "product_name" in request_data:
        item["product_name"] = str(request_data["product_name"])
    
    if "brands" in request_data:
        item["brands"] = str(request_data["brands"])
    
    if "barcode" in request_data:
        item["barcode"] = str(request_data["barcode"])
    
    if "ingredients_text" in request_data:
        item["ingredients_text"] = str(request_data["ingredients_text"])
    
    if "price" in request_data:
        item["price"] = float(request_data["price"])
    
    if "quantity" in request_data:
        item["quantity"] = int(request_data["quantity"])
    
    return jsonify({
        "status": "success",
        "message": "Item updated successfully",
        "data": item
    }), 200


@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    """
    DELETE /inventory/<id> - Delete an inventory item
    
    Args:
        item_id (int): The ID of the item to delete
        
    Returns:
        JSON with status message (200 if successful, 404 if item not found)
    """
    global inventory
    
    # Find and remove the item
    item = find_item(item_id)
    
    if not item:
        return jsonify({
            "status": "error",
            "message": f"Item with ID {item_id} not found"
        }), 404
    
    inventory.remove(item)
    
    return jsonify({
        "status": "success",
        "message": "Item deleted successfully"
    }), 200


@app.route('/search-external', methods=['POST'])
def search_external_api():
    """
    POST /search-external - Search OpenFoodFacts API for product data
    
    Request JSON should contain either:
        - barcode (string): Product barcode for specific product search
        - product_name (string): Product name for general search
        
    Returns:
        JSON with status and product data from OpenFoodFacts API
        (200 if successful, 400 if missing params, 500 if API error)
    """
    request_data = request.get_json()
    
    # Check if request has data and at least one search parameter
    if not request_data or not (request_data.get("barcode") or request_data.get("product_name")):
        return jsonify({
            "status": "error",
            "message": "Please provide either 'barcode' or 'product_name'"
        }), 400
    
    try:
        # Search by barcode if provided, otherwise search by name
        if request_data.get("barcode"):
            search_result = search_by_barcode(request_data["barcode"])
        else:
            search_result = search_by_name(request_data["product_name"])
        
        return jsonify({
            "status": "success",
            "data": search_result
        }), 200
        
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


def search_by_barcode(barcode):
    """
    Search OpenFoodFacts API for a product using its barcode.
    
    Args:
        barcode (string): The product barcode to search for
        
    Returns:
        dict: Product information including name, brand, ingredients, etc.
        
    Raises:
        Exception: If product not found or API request fails
    """
    # Call OpenFoodFacts API with barcode
    api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(api_url, timeout=5)
    api_data = response.json()
    
    # Check if product was found
    if api_data.get("status") == 1 and "product" in api_data:
        product = api_data["product"]
        
        # Extract relevant product information
        return {
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", ""),
            "barcode": barcode,
            "ingredients_text": product.get("ingredients_text", ""),
            "quantity": product.get("quantity", ""),
            "image_url": product.get("image_url", "")
        }
    
    raise Exception(f"Product not found for barcode: {barcode}")


def search_by_name(product_name):
    """
    Search OpenFoodFacts API for products by name.
    
    Args:
        product_name (string): The product name to search for
        
    Returns:
        list: List of up to 5 matching products with their information
        
    Raises:
        Exception: If no products found or API request fails
    """
    # Call OpenFoodFacts API with product name search
    api_url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }
    
    response = requests.get(api_url, params=params, timeout=5)
    api_data = response.json()
    
    # Check if products were found
    if "products" in api_data and len(api_data["products"]) > 0:
        # Extract information from up to 5 results
        results = []
        for product in api_data["products"][:5]:
            results.append({
                "product_name": product.get("product_name", ""),
                "brands": product.get("brands", ""),
                "barcode": product.get("code", ""),
                "ingredients_text": product.get("ingredients_text", ""),
                "quantity": product.get("quantity", ""),
                "image_url": product.get("image_url", "")
            })
        return results
    
    raise Exception(f"No products found for: {product_name}")


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 - Endpoint Not Found errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found. Please check your URL and HTTP method."
    }), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """Handle 405 - Method Not Allowed errors"""
    return jsonify({
        "status": "error",
        "message": "Method not allowed. Please check the HTTP method for this endpoint."
    }), 405


@app.errorhandler(500)
def server_error(error):
    """Handle 500 - Internal Server errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error. Something went wrong on our end."
    }), 500


# ============= MAIN =============

if __name__ == '__main__':
    # Run Flask development server
    # Debug mode enabled for development
    app.run(debug=True, host='0.0.0.0', port=5000)
