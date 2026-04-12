"""
Inventory Management System - Flask REST API
A simple REST API for managing inventory items with external API integration.
"""

from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Mock database - stores inventory items as a list
# Each item has an ID, name, brand, price, quantity, and other details
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "barcode": "5901234123457",
        "price": 3.99,
        "quantity": 45,
        "ingredients_text": "Filtered water, almonds, cane sugar, salt, potassium chloride",
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

# Helper function to get the next available ID
def get_next_id():
    """Get the next available ID for a new inventory item"""
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


# ===== GET ENDPOINTS =====

@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    """
    Fetch all inventory items
    Returns: JSON list of all inventory items
    """
    return jsonify({
        "status": "success",
        "count": len(inventory),
        "data": inventory
    }), 200


@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    """
    Fetch a single inventory item by ID
    Args: item_id (int) - The ID of the item to retrieve
    Returns: JSON object of the requested item or 404 error
    """
    for item in inventory:
        if item["id"] == item_id:
            return jsonify({
                "status": "success",
                "data": item
            }), 200
    
    return jsonify({
        "status": "error",
        "message": f"Item with ID {item_id} not found"
    }), 404


# ===== POST ENDPOINT =====

@app.route('/inventory', methods=['POST'])
def create_inventory_item():
    """
    Add a new inventory item to the database
    Request body should contain: product_name, brands, price, quantity, barcode (optional)
    Returns: JSON object of the newly created item
    """
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(key in data for key in ["product_name", "brands", "price", "quantity"]):
        return jsonify({
            "status": "error",
            "message": "Missing required fields: product_name, brands, price, quantity"
        }), 400
    
    # Create new item with auto-generated ID
    new_item = {
        "id": get_next_id(),
        "product_name": data["product_name"],
        "brands": data["brands"],
        "barcode": data.get("barcode", ""),
        "price": float(data["price"]),
        "quantity": int(data["quantity"]),
        "ingredients_text": data.get("ingredients_text", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    inventory.append(new_item)
    
    return jsonify({
        "status": "success",
        "message": "Item created successfully",
        "data": new_item
    }), 201


# ===== PATCH ENDPOINT =====

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    """
    Update an existing inventory item (supports partial updates)
    Can update: product_name, brands, price, quantity, ingredients_text
    Returns: JSON object of the updated item or 404 error
    """
    data = request.get_json()
    
    for item in inventory:
        if item["id"] == item_id:
            # Update fields if provided in request
            if "product_name" in data:
                item["product_name"] = data["product_name"]
            if "brands" in data:
                item["brands"] = data["brands"]
            if "price" in data:
                item["price"] = float(data["price"])
            if "quantity" in data:
                item["quantity"] = int(data["quantity"])
            if "ingredients_text" in data:
                item["ingredients_text"] = data["ingredients_text"]
            if "barcode" in data:
                item["barcode"] = data["barcode"]
            
            return jsonify({
                "status": "success",
                "message": "Item updated successfully",
                "data": item
            }), 200
    
    return jsonify({
        "status": "error",
        "message": f"Item with ID {item_id} not found"
    }), 404


# ===== DELETE ENDPOINT =====

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    """
    Delete an inventory item by ID
    Args: item_id (int) - The ID of the item to delete
    Returns: Success message or 404 error
    """
    global inventory
    
    for i, item in enumerate(inventory):
        if item["id"] == item_id:
            deleted_item = inventory.pop(i)
            return jsonify({
                "status": "success",
                "message": "Item deleted successfully",
                "data": deleted_item
            }), 200
    
    return jsonify({
        "status": "error",
        "message": f"Item with ID {item_id} not found"
    }), 404


# ===== HELPER ROUTE FOR EXTERNAL API =====

@app.route('/search-external', methods=['POST'])
def search_external_api():
    """
    Search for product data from OpenFoodFacts API by barcode or product name
    Request body: {"barcode": "123456"} or {"product_name": "milk"}
    Returns: Product data from external API or error message
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400
    
    barcode = data.get("barcode")
    product_name = data.get("product_name")
    
    if not barcode and not product_name:
        return jsonify({
            "status": "error",
            "message": "Either 'barcode' or 'product_name' is required"
        }), 400
    
    try:
        if barcode:
            # Search by barcode
            result = search_product_by_barcode(barcode)
        else:
            # Search by product name
            result = search_product_by_name(product_name)
        
        return jsonify({
            "status": "success",
            "data": result
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


def search_product_by_barcode(barcode):
    """
    Search OpenFoodFacts API for product by barcode
    Args: barcode (str) - Product barcode
    Returns: Product data dictionary
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") == 1 and "product" in data:
            product = data["product"]
            return {
                "product_name": product.get("product_name", ""),
                "brands": product.get("brands", ""),
                "barcode": barcode,
                "ingredients_text": product.get("ingredients_text", ""),
                "quantity": product.get("quantity", ""),
                "image_url": product.get("image_url", "")
            }
        else:
            raise Exception(f"Product not found for barcode: {barcode}")
    
    except requests.exceptions.Timeout:
        raise Exception("API request timed out")
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def search_product_by_name(product_name):
    """
    Search OpenFoodFacts API for products by name
    Args: product_name (str) - Product name to search for
    Returns: List of product data dictionaries
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if "products" in data and len(data["products"]) > 0:
            # Return first 5 results
            results = []
            for product in data["products"][:5]:
                results.append({
                    "product_name": product.get("product_name", ""),
                    "brands": product.get("brands", ""),
                    "barcode": product.get("code", ""),
                    "ingredients_text": product.get("ingredients_text", ""),
                    "quantity": product.get("quantity", ""),
                    "image_url": product.get("image_url", "")
                })
            return results
        else:
            raise Exception(f"No products found for: {product_name}")
    
    except requests.exceptions.Timeout:
        raise Exception("API request timed out")
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors (method not allowed)"""
    return jsonify({
        "status": "error",
        "message": "Method not allowed"
    }), 405


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Run the Flask app in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
