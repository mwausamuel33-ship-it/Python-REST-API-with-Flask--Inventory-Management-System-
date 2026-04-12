"""
CLI Tool for Inventory Management API
Connect to Flask REST API and do CRUD operations through command line
"""

import requests
import json
from typing import Dict, Any

# URL for Flask API server
BASE_URL = "http://localhost:5000"


def print_header(text):
    # Print a nice looking header
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_success(message):
    # Green success message
    print(f"✓ {message}")


def print_error(message):
    # Red error message
    print(f"✗ Error: {message}")


def print_info(message):
    # Info message
    print(f"ℹ {message}")


def format_item(item: Dict[str, Any]):
    # Format item nicely for display
    print(f"\n  ID: {item['id']}")
    print(f"  Product: {item['product_name']}")
    print(f"  Brand: {item['brands']}")
    print(f"  Barcode: {item['barcode']}")
    print(f"  Price: ${item['price']:.2f}")
    print(f"  Quantity: {item['quantity']}")
    print(f"  Ingredients: {item['ingredients_text']}")
    print(f"  Created: {item['created_at']}")


def get_all_inventory():
    # Get and display all items
    print_header("View All Inventory Items")
    
    try:
        response = requests.get(f"{BASE_URL}/inventory", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "success":
            items = data["data"]
            print_success(f"Retrieved {data['count']} items")
            
            if len(items) == 0:
                print_info("No items in inventory")
            else:
                for item in items:
                    format_item(item)
        else:
            print_error(f"API returned error: {data.get('message', 'Unknown error')}")
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to the API. Make sure the server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Failed to retrieve inventory: {str(e)}")


def get_single_item():
    # Get one item by ID
    print_header("View Single Inventory Item")
    
    try:
        item_id = int(input("  Enter Item ID: "))
    except ValueError:
        print_error("Invalid ID format. Please enter a number.")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "success":
            print_success(f"Item {item_id} found")
            format_item(data["data"])
        else:
            print_error(data.get("message", "Unknown error"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to the API. Make sure the server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Failed to retrieve item: {str(e)}")


def add_new_item():
    # Add item to inventory
    print_header("Add New Inventory Item")
    
    try:
        product_name = input("  Product Name: ").strip()
        brands = input("  Brand: ").strip()
        barcode = input("  Barcode (optional): ").strip()
        
        try:
            price = float(input("  Price ($): "))
            quantity = int(input("  Quantity: "))
        except ValueError:
            print_error("Price must be a number and Quantity must be an integer")
            return
        
        ingredients = input("  Ingredients (optional): ").strip()
        
        # Validate
        if not product_name or not brands or price < 0 or quantity < 0:
            print_error("Please fill in all required fields with valid values")
            return
        
        # Create payload
        payload = {
            "product_name": product_name,
            "brands": brands,
            "price": price,
            "quantity": quantity
        }
        
        if barcode:
            payload["barcode"] = barcode
        if ingredients:
            payload["ingredients_text"] = ingredients
        
        # Send to API
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "success":
            print_success(data["message"])
            print(f"  New Item ID: {data['data']['id']}")
            format_item(data["data"])
        else:
            print_error(data.get("message", "Unknown error"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to the API. Make sure the server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Failed to add item: {str(e)}")


def update_item():
    # Update existing item
    print_header("Update Inventory Item")
    
    try:
        item_id = int(input("  Enter Item ID to update: "))
    except ValueError:
        print_error("Invalid ID format. Please enter a number.")
        return
    
    print("\n  Leave field empty to skip updating it")
    
    try:
        product_name = input("  Product Name (optional): ").strip()
        brands = input("  Brand (optional): ").strip()
        barcode = input("  Barcode (optional): ").strip()
        
        price_input = input("  Price $ (optional): ").strip()
        quantity_input = input("  Quantity (optional): ").strip()
        ingredients = input("  Ingredients (optional): ").strip()
        
        # Build payload with only provided fields
        payload = {}
        
        if product_name:
            payload["product_name"] = product_name
        if brands:
            payload["brands"] = brands
        if barcode:
            payload["barcode"] = barcode
        if ingredients:
            payload["ingredients_text"] = ingredients
        
        if price_input:
            try:
                payload["price"] = float(price_input)
            except ValueError:
                print_error("Price must be a valid number")
                return
        
        if quantity_input:
            try:
                payload["quantity"] = int(quantity_input)
            except ValueError:
                print_error("Quantity must be a valid integer")
                return
        
        if not payload:
            print_error("No fields to update")
            return
        
        # Send PATCH request
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "success":
            print_success(data["message"])
            format_item(data["data"])
        else:
            print_error(data.get("message", "Unknown error"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to the API. Make sure the server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Failed to update item: {str(e)}")


def delete_item():
    # Delete item from inventory
    print_header("Delete Inventory Item")
    
    try:
        item_id = int(input("  Enter Item ID to delete: "))
    except ValueError:
        print_error("Invalid ID format. Please enter a number.")
        return
    
    confirm = input(f"  Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print_info("Deletion cancelled")
        return
    
    try:
        response = requests.delete(
            f"{BASE_URL}/inventory/{item_id}",
            timeout=5
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "success":
            print_success(data["message"])
            print(f"  Deleted item ID: {data['data']['id']}")
        else:
            print_error(data.get("message", "Unknown error"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to the API. Make sure the server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Failed to delete item: {str(e)}")


def search_external_api():
    # Search OpenFoodFacts API
    print_header("Search External API (OpenFoodFacts)")
    
    search_type = input("  Search by (1) Barcode or (2) Product Name? Enter 1 or 2: ").strip()
    
    if search_type == '1':
        barcode = input("  Enter Barcode: ").strip()
        if not barcode:
            print_error("Barcode cannot be empty")
            return
        payload = {"barcode": barcode}
    elif search_type == '2':
        product_name = input("  Enter Product Name: ").strip()
        if not product_name:
            print_error("Product name cannot be empty")
            return
        payload = {"product_name": product_name}
    else:
        print_error("Invalid choice. Please enter 1 or 2.")
        return
    
    try:
        response = requests.post(
            f"{BASE_URL}/search-external",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "success":
            results = data["data"]
            
            if isinstance(results, list):
                print_success(f"Found {len(results)} product(s)")
                for i, product in enumerate(results, 1):
                    print(f"\n  Result {i}:")
                    print(f"    Name: {product['product_name']}")
                    print(f"    Brand: {product['brands']}")
                    print(f"    Barcode: {product['barcode']}")
                    print(f"    Ingredients: {product['ingredients_text']}")
                    print(f"    Quantity: {product['quantity']}")
            else:
                print_success("Product found")
                print(f"  Name: {results['product_name']}")
                print(f"  Brand: {results['brands']}")
                print(f"  Barcode: {results['barcode']}")
                print(f"  Ingredients: {results['ingredients_text']}")
                print(f"  Quantity: {results['quantity']}")
                
                # Ask to add to inventory
                add_to_inv = input("\n  Add this product to inventory? (yes/no): ").strip().lower()
                if add_to_inv == 'yes':
                    try:
                        qty = int(input("  Quantity to add: "))
                        price = float(input("  Price ($): "))
                        
                        add_payload = {
                            "product_name": results['product_name'],
                            "brands": results['brands'],
                            "barcode": results['barcode'],
                            "ingredients_text": results['ingredients_text'],
                            "quantity": qty,
                            "price": price
                        }
                        
                        add_response = requests.post(
                            f"{BASE_URL}/inventory",
                            json=add_payload,
                            timeout=5
                        )
                        add_response.raise_for_status()
                        
                        add_data = add_response.json()
                        if add_data["status"] == "success":
                            print_success(f"Product added to inventory with ID: {add_data['data']['id']}")
                        else:
                            print_error(add_data.get("message", "Failed to add product"))
                    
                    except ValueError:
                        print_error("Invalid quantity or price format")
                    except Exception as e:
                        print_error(f"Failed to add product: {str(e)}")
        else:
            print_error(data.get("message", "API search failed"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to the API. Make sure the server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print_error("Request timed out - API may be slow")
    except Exception as e:
        print_error(f"Search failed: {str(e)}")


def show_menu():
    # Display main menu
    print_header("Inventory Management System - CLI")
    print("""
  1. View all inventory items
  2. View single item by ID
  3. Add new inventory item
  4. Update inventory item
  5. Delete inventory item
  6. Search external API (OpenFoodFacts)
  7. Exit
    """)


def main():
    # Main loop for CLI
    print("\n" + "="*60)
    print("  Welcome to Inventory Management System CLI")
    print("  Make sure the Flask server is running on localhost:5000")
    print("="*60)
    
    while True:
        show_menu()
        choice = input("  Enter your choice (1-7): ").strip()
        
        if choice == '1':
            get_all_inventory()
        elif choice == '2':
            get_single_item()
        elif choice == '3':
            add_new_item()
        elif choice == '4':
            update_item()
        elif choice == '5':
            delete_item()
        elif choice == '6':
            search_external_api()
        elif choice == '7':
            print_success("Goodbye!")
            break
        else:
            print_error("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == '__main__':
    main()
