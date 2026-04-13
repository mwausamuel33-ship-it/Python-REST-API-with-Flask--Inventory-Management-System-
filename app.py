"""Inventory Management System - REST API with Flask"""

from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

inventory = [
    {"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk", "barcode": "5901234123457", "price": 3.99, "quantity": 45, "ingredients_text": "Filtered water, almonds, cane sugar", "created_at": "2024-01-15"},
    {"id": 2, "product_name": "Whole Wheat Bread", "brands": "Nature's Best", "barcode": "5901234123458", "price": 2.49, "quantity": 30, "ingredients_text": "Flour, water, yeast, salt", "created_at": "2024-01-20"}
]


def get_next_id():
    return max((item["id"] for item in inventory), default=0) + 1


def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    return jsonify({"status": "success", "count": len(inventory), "data": inventory}), 200


@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    item = find_item(item_id)
    if item:
        return jsonify({"status": "success", "data": item}), 200
    return jsonify({"status": "error", "message": f"Item {item_id} not found"}), 404


@app.route('/inventory', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    if not data or not all(k in data for k in ["product_name", "brands", "price", "quantity"]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
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
    return jsonify({"status": "success", "message": "Item created", "data": new_item}), 201


@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"status": "error", "message": f"Item {item_id} not found"}), 404
    
    data = request.get_json()
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
    
    return jsonify({"status": "success", "message": "Item updated", "data": item}), 200


@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    global inventory
    for i, item in enumerate(inventory):
        if item["id"] == item_id:
            deleted = inventory.pop(i)
            return jsonify({"status": "success", "message": "Item deleted", "data": deleted}), 200
    return jsonify({"status": "error", "message": f"Item {item_id} not found"}), 404


@app.route('/search-external', methods=['POST'])
def search_external_api():
    data = request.get_json()
    if not data or not (data.get("barcode") or data.get("product_name")):
        return jsonify({"status": "error", "message": "Barcode or product_name required"}), 400
    
    try:
        result = search_by_barcode(data["barcode"]) if data.get("barcode") else search_by_name(data["product_name"])
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def search_by_barcode(barcode):
    response = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json", timeout=5)
    data = response.json()
    if data.get("status") == 1 and "product" in data:
        p = data["product"]
        return {"product_name": p.get("product_name", ""), "brands": p.get("brands", ""), "barcode": barcode, "ingredients_text": p.get("ingredients_text", ""), "quantity": p.get("quantity", ""), "image_url": p.get("image_url", "")}
    raise Exception(f"Product not found: {barcode}")


def search_by_name(product_name):
    response = requests.get("https://world.openfoodfacts.org/cgi/search.pl", params={"search_terms": product_name, "search_simple": 1, "action": "process", "json": 1}, timeout=5)
    data = response.json()
    if "products" in data and len(data["products"]) > 0:
        return [{"product_name": p.get("product_name", ""), "brands": p.get("brands", ""), "barcode": p.get("code", ""), "ingredients_text": p.get("ingredients_text", ""), "quantity": p.get("quantity", ""), "image_url": p.get("image_url", "")} for p in data["products"][:5]]
    raise Exception(f"No products found: {product_name}")


@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
