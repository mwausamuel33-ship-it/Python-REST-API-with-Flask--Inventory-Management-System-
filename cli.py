"""
Inventory Management System - Command Line Interface (CLI)
This CLI tool allows users to interact with the Inventory API.
Users can view, add, update, and delete inventory items,
as well as search for product information from the external API.
"""

import requests
import json

# API server base URL
BASE_URL = "http://localhost:5000"


def print_header(title):
    """Print a formatted header for the menu"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_success(message):
    """Print success message in green"""
    print(f"\n✓ SUCCESS: {message}")


def print_error(message):
    """Print error message"""
    print(f"\n✗ ERROR: {message}")


def print_info(message):
    """Print info message"""
    print(f"ℹ INFO: {message}")


def display_menu():
    """Display the main menu options"""
    print_header("INVENTORY MANAGEMENT SYSTEM")
    print("""
  1. View All Items
  2. View Single Item by ID
  3. Add New Item
  4. Update Item
  5. Delete Item
  6. Search External API (OpenFoodFacts)
  7. Exit
    """)


def view_all_items():
    """Retrieve and display all inventory items"""
    print_header("ALL INVENTORY ITEMS")
    
    try:
        response = requests.get(f"{BASE_URL}/inventory", timeout=5)
        data = response.json()
        
        if data["status"] == "success":
            items = data.get("data", [])
            print_success(f"Retrieved {data['count']} items")
            
            if len(items) == 0:
                print_info("No items in inventory")
            else:
                # Display each item with formatting
                for item in items:
                    print(f"\n  ID: {item['id']}")
                    print(f"  Product Name: {item['product_name']}")
                    print(f"  Brand: {item['brands']}")
                    print(f"  Price: ${item['price']:.2f}")
                    print(f"  Quantity: {item['quantity']}")
                    print(f"  Barcode: {item['barcode']}")
                    print(f"  Created: {item['created_at']}")
        else:
            print_error(data.get("message", "Failed to retrieve items"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API server. Is it running on localhost:5000?")
    except Exception as error:
        print_error(f"Failed to retrieve inventory: {str(error)}")


def view_single_item():
    """Retrieve and display a single item by ID"""
    print_header("VIEW SINGLE ITEM")
    
    try:
        item_id = int(input("  Enter Item ID: "))
    except ValueError:
        print_error("Item ID must be a number")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}", timeout=5)
        data = response.json()
        
        if data["status"] == "success":
            item = data["data"]
            print_success(f"Item {item_id} found")
            
            print(f"\n  ID: {item['id']}")
            print(f"  Product Name: {item['product_name']}")
            print(f"  Brand: {item['brands']}")
            print(f"  Price: ${item['price']:.2f}")
            print(f"  Quantity: {item['quantity']}")
            print(f"  Barcode: {item['barcode']}")
            print(f"  Ingredients: {item['ingredients_text']}")
            print(f"  Created: {item['created_at']}")
        else:
            print_error(data.get("message", "Item not found"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API server")
    except Exception as error:
        print_error(f"Failed to retrieve item: {str(error)}")


def add_new_item():
    """Add a new item to the inventory"""
    print_header("ADD NEW ITEM")
    
    try:
        # Get product information from user
        product_name = input("  Product Name: ").strip()
        brand = input("  Brand: ").strip()
        barcode = input("  Barcode (optional): ").strip()
        
        # Get price and quantity with type validation
        try:
            price = float(input("  Price ($): "))
            quantity = int(input("  Quantity: "))
        except ValueError:
            print_error("Price must be a number and Quantity must be a whole number")
            return
        
        ingredients = input("  Ingredients (optional): ").strip()
        
        # Validate required fields
        if not product_name or not brand:
            print_error("Product name and brand are required")
            return
        
        if price < 0 or quantity < 0:
            print_error("Price and quantity must be positive numbers")
            return
        
        # Create request payload
        payload = {
            "product_name": product_name,
            "brands": brand,
            "price": price,
            "quantity": quantity
        }
        
        # Add optional fields if provided
        if barcode:
            payload["barcode"] = barcode
        if ingredients:
            payload["ingredients_text"] = ingredients
        
        # Send request to API
        response = requests.post(f"{BASE_URL}/inventory", json=payload, timeout=5)
        data = response.json()
        
        if data["status"] == "success":
            new_item = data["data"]
            print_success(f"Item added successfully (ID: {new_item['id']})")
            print(f"\n  Product: {new_item['product_name']}")
            print(f"  Brand: {new_item['brands']}")
            print(f"  Price: ${new_item['price']:.2f}")
            print(f"  Quantity: {new_item['quantity']}")
        else:
            print_error(data.get("message", "Failed to add item"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API server")
    except Exception as error:
        print_error(f"Failed to add item: {str(error)}")


def update_item():
    """Update an existing inventory item"""
    print_header("UPDATE ITEM")
    
    try:
        item_id = int(input("  Enter Item ID to update: "))
    except ValueError:
        print_error("Item ID must be a number")
        return
    
    print("\n  Leave fields empty to skip updating them")
    
    try:
        # Get updated information from user
        product_name = input("  Product Name (optional): ").strip()
        brand = input("  Brand (optional): ").strip()
        barcode = input("  Barcode (optional): ").strip()
        
        price_input = input("  Price $ (optional): ").strip()
        quantity_input = input("  Quantity (optional): ").strip()
        ingredients = input("  Ingredients (optional): ").strip()
        
        # Build payload with only provided fields
        payload = {}
        
        if product_name:
            payload["product_name"] = product_name
        if brand:
            payload["brands"] = brand
        if barcode:
            payload["barcode"] = barcode
        if ingredients:
            payload["ingredients_text"] = ingredients
        
        # Validate numeric inputs
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
                print_error("Quantity must be a valid whole number")
                return
        
        # Check if any fields were provided
        if not payload:
            print_error("No fields to update")
            return
        
        # Send PATCH request to API
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload, timeout=5)
        data = response.json()
        
        if data["status"] == "success":
            print_success("Item updated successfully")
            item = data["data"]
            print(f"\n  Updated Item {item['id']}:")
            print(f"  Product: {item['product_name']}")
            print(f"  Brand: {item['brands']}")
            print(f"  Price: ${item['price']:.2f}")
            print(f"  Quantity: {item['quantity']}")
        else:
            print_error(data.get("message", "Failed to update item"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API server")
    except Exception as error:
        print_error(f"Failed to update item: {str(error)}")


def delete_item():
    """Delete an item from the inventory"""
    print_header("DELETE ITEM")
    
    try:
        item_id = int(input("  Enter Item ID to delete: "))
    except ValueError:
        print_error("Item ID must be a number")
        return
    
    # Confirm deletion
    confirm = input(f"\n  Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print_info("Deletion cancelled")
        return
    
    try:
        # Send DELETE request to API
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}", timeout=5)
        data = response.json()
        
        if data["status"] == "success":
            print_success(f"Item {item_id} deleted successfully")
        else:
            print_error(data.get("message", "Failed to delete item"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API server")
    except Exception as error:
        print_error(f"Failed to delete item: {str(error)}")


def search_external_api():
    """Search OpenFoodFacts API for product information"""
    print_header("SEARCH EXTERNAL API (OpenFoodFacts)")
    
    print("\n  Search by:")
    print("  1. Barcode")
    print("  2. Product Name")
    
    search_type = input("\n  Enter choice (1 or 2): ").strip()
    
    if search_type == "1":
        barcode = input("  Enter Barcode: ").strip()
        if not barcode:
            print_error("Barcode cannot be empty")
            return
        payload = {"barcode": barcode}
    
    elif search_type == "2":
        product_name = input("  Enter Product Name: ").strip()
        if not product_name:
            print_error("Product name cannot be empty")
            return
        payload = {"product_name": product_name}
    
    else:
        print_error("Invalid choice. Please enter 1 or 2")
        return
    
    try:
        # Send search request to API
        response = requests.post(f"{BASE_URL}/search-external", json=payload, timeout=10)
        data = response.json()
        
        if data["status"] == "success":
            results = data["data"]
            
            # Handle both single result and multiple results
            if isinstance(results, list):
                print_success(f"Found {len(results)} product(s)")
                
                for i, product in enumerate(results, 1):
                    print(f"\n  Result {i}:")
                    print(f"    Name: {product['product_name']}")
                    print(f"    Brand: {product['brands']}")
                    print(f"    Barcode: {product['barcode']}")
                    print(f"    Ingredients: {product['ingredients_text']}")
            
            else:
                # Single product result
                print_success("Product found")
                product = results
                print(f"\n  Name: {product['product_name']}")
                print(f"  Brand: {product['brands']}")
                print(f"  Barcode: {product['barcode']}")
                print(f"  Ingredients: {product['ingredients_text']}")
        
        else:
            print_error(data.get("message", "Search failed"))
    
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to API server")
    except requests.exceptions.Timeout:
        print_error("API request timed out. OpenFoodFacts API may be slow.")
    except Exception as error:
        print_error(f"Search failed: {str(error)}")


def main():
    """Main function - runs the CLI application loop"""
    print("\n" + "=" * 60)
    print("  Welcome to Inventory Management System")
    print("  Server: localhost:5000")
    print("=" * 60)
    
    # Main menu loop
    while True:
        try:
            display_menu()
            choice = input("  Enter your choice (1-7): ").strip()
            
            if choice == "1":
                view_all_items()
            elif choice == "2":
                view_single_item()
            elif choice == "3":
                add_new_item()
            elif choice == "4":
                update_item()
            elif choice == "5":
                delete_item()
            elif choice == "6":
                search_external_api()
            elif choice == "7":
                print_success("Thank you for using Inventory Management System. Goodbye!")
                break
            else:
                print_error("Invalid choice. Please enter a number between 1 and 7")
        
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            break
        except Exception as error:
            print_error(f"An unexpected error occurred: {str(error)}")


if __name__ == "__main__":
    main()
