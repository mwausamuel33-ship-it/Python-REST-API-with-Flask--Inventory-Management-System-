from flask import Flask,request,jsonify
import requests
from datetime import datetime

app = Flask(__name__)

inventory=[{"id":1,"product_name":"Organic Almond Milk","brands":"Silk","barcode":"5901234123457","price":3.99,"quantity":45,"ingredients_text":"Filtered water, almonds, cane sugar","created_at":"2024-01-15"},{"id":2,"product_name":"Whole Wheat Bread","brands":"Nature's Best","barcode":"5901234123458","price":2.49,"quantity":30,"ingredients_text":"Flour, water, yeast, salt","created_at":"2024-01-20"}]


def get_next_id():
    return max((i["id"] for i in inventory), default=0)+1


def find_item(item_id):
    for i in inventory:
        if i["id"]==item_id:
            return i
    return None


@app.route('/')
def home():
    return jsonify({"status":"success","message":"Welcome to Inventory Management API"}),200

@app.route('/inventory',methods=['GET'])
def get_all_inventory():
    return jsonify({"status":"success","count":len(inventory),"data":inventory}),200


@app.route('/inventory/<int:item_id>',methods=['GET'])
def get_inventory_item(item_id):
    i=find_item(item_id)
    if i:return jsonify({"status":"success","data":i}),200
    return jsonify({"status":"error","message":f"Item {item_id} not found"}),404


@app.route('/inventory',methods=['POST'])
def create_inventory_item():
    d=request.get_json()
    if not d or not all(k in d for k in["product_name","brands","price","quantity"]):return jsonify({"status":"error","message":"Missing required fields"}),400
    ni={"id":get_next_id(),"product_name":d["product_name"],"brands":d["brands"],"barcode":d.get("barcode",""),"price":float(d["price"]),"quantity":int(d["quantity"]),"ingredients_text":d.get("ingredients_text",""),"created_at":datetime.now().strftime("%Y-%m-%d")}
    inventory.append(ni)
    return jsonify({"status":"success","message":"Item created","data":ni}),201





@app.route('/search-external',methods=['POST'])
def search_external_api():
    d=request.get_json()
    if not d or not(d.get("barcode")or d.get("product_name")):return jsonify({"status":"error","message":"Barcode or product_name required"}),400
    try:
        r=search_by_barcode(d["barcode"])if d.get("barcode")else search_by_name(d["product_name"])
        return jsonify({"status":"success","data":r}),200
    except Exception as e:return jsonify({"status":"error","message":str(e)}),500


def search_by_barcode(barcode):
    r=requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json",timeout=5)
    d=r.json()
    if d.get("status")==1 and"product"in d:
        p=d["product"]
        return {"product_name":p.get("product_name", ""),"brands":p.get("brands", ""),"barcode":barcode,"ingredients_text":p.get("ingredients_text", ""),"quantity":p.get("quantity", ""),"image_url":p.get("image_url", "")}
    raise Exception(f"Product not found: {barcode}")


def search_by_name(product_name):
    r=requests.get("https://world.openfoodfacts.org/cgi/search.pl",params={"search_terms":product_name,"search_simple":1,"action":"process","json":1},timeout=5)
    d=r.json()
    if"products"in d and len(d["products"])>0:
        return [{"product_name":p.get("product_name", ""),"brands":p.get("brands", ""),"barcode":p.get("code", ""),"ingredients_text":p.get("ingredients_text", ""),"quantity":p.get("quantity", ""),"image_url":p.get("image_url", "")}for p in d["products"][:5]]
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
