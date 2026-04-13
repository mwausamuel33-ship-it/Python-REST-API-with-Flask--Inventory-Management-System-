"""CLI for Inventory Management API"""

import requests

BASE_URL = "http://localhost:5000"


def print_msg(text, msg_type="info"):
    if msg_type == "header":
        print("\n" + "="*60 + f"\n  {text}\n" + "="*60)
    elif msg_type == "success":
        print(f"✓ {text}")
    elif msg_type == "error":
        print(f"✗ {text}")
    else:
        print(f"ℹ {text}")


def api_request(method, endpoint, data=None):
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(method, url, json=data, timeout=5)
        return response.json()
    except Exception as error:
        return {"status": "error", "message": str(error)}


def show_item(item):
    print(f"  [{item['id']}] {item['product_name']} | ${item['price']:.2f} | Qty: {item['quantity']}")


def view_all():
    print_msg("All Items", "header")
    data = api_request("GET", "/inventory")
    if data["status"] == "success":
        for item in data.get("data", []):
            show_item(item)
    else:
        print_msg(data.get("message"), "error")


def view_one():
    print_msg("Get Item", "header")
    try:
        item_id = int(input("  ID: "))
        data = api_request("GET", f"/inventory/{item_id}")
        if data["status"] == "success":
            show_item(data["data"])
        else:
            print_msg(data.get("message"), "error")
    except ValueError:
        print_msg("Invalid ID", "error")


def add_item():
    print_msg("Add Item", "header")
    try:
        product = input("  Product: ").strip()
        brand = input("  Brand: ").strip()
        price = float(input("  Price: "))
        qty = int(input("  Quantity: "))
        
        if not product or not brand:
            print_msg("Product and brand required", "error")
            return
        
        payload = {"product_name": product, "brands": brand, "price": price, "quantity": qty}
        data = api_request("POST", "/inventory", payload)
        
        if data["status"] == "success":
            print_msg("Item added", "success")
        else:
            print_msg(data.get("message"), "error")
    except ValueError:
        print_msg("Invalid input", "error")


def delete_item():
    print_msg("Delete Item", "header")
    try:
        item_id = int(input("  ID: "))
        confirm = input(f"  Confirm? (yes/no): ").lower()
        if confirm == "yes":
            data = api_request("DELETE", f"/inventory/{item_id}")
            if data["status"] == "success":
                print_msg("Deleted", "success")
            else:
                print_msg(data.get("message"), "error")
    except ValueError:
        print_msg("Invalid ID", "error")


def main():
    print("\n" + "="*60)
    print("  Inventory CLI - localhost:5000")
    print("="*60)
    
    while True:
        print("\n  1. All items  2. Get item  3. Add  4. Delete  5. Exit")
        choice = input("  Choice (1-5): ").strip()
        
        if choice == "1":
            view_all()
        elif choice == "2":
            view_one()
        elif choice == "3":
            add_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            print_msg("Goodbye!", "success")
            break
        else:
            print_msg("Invalid choice", "error")


if __name__ == "__main__":
    main()
