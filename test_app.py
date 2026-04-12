"""
Unit Tests for Inventory Management System
Tests for Flask API endpoints and external API integration
"""

import pytest
import json
from app import app, inventory, get_next_id


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_inventory():
    """Reset inventory before each test"""
    # Store original inventory
    original = inventory.copy()
    
    # Clear and reset inventory
    inventory.clear()
    inventory.extend([
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
            "ingredients_text": "Whole wheat flour, water, yeast",
            "created_at": "2024-01-20"
        }
    ])
    
    yield
    
    # Restore original inventory after test
    inventory.clear()
    inventory.extend(original)


# ===== GET ENDPOINT TESTS =====

def test_get_all_inventory(client, setup_inventory):
    """Test fetching all inventory items"""
    response = client.get('/inventory')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['status'] == 'success'
    assert data['count'] == 2
    assert len(data['data']) == 2


def test_get_single_item_success(client, setup_inventory):
    """Test fetching a single item by ID"""
    response = client.get('/inventory/1')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['status'] == 'success'
    assert data['data']['id'] == 1
    assert data['data']['product_name'] == 'Organic Almond Milk'


def test_get_single_item_not_found(client, setup_inventory):
    """Test fetching a non-existent item"""
    response = client.get('/inventory/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    
    assert data['status'] == 'error'
    assert 'not found' in data['message']


# ===== POST ENDPOINT TESTS =====

def test_create_item_success(client, setup_inventory):
    """Test creating a new inventory item"""
    new_item = {
        "product_name": "Greek Yogurt",
        "brands": "Fage",
        "price": 4.99,
        "quantity": 20,
        "barcode": "5901234123459",
        "ingredients_text": "Milk, cultures"
    }
    
    response = client.post(
        '/inventory',
        data=json.dumps(new_item),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert data['status'] == 'success'
    assert data['data']['product_name'] == 'Greek Yogurt'
    assert data['data']['id'] == 3  # Should be auto-incremented


def test_create_item_missing_required_field(client, setup_inventory):
    """Test creating an item with missing required fields"""
    incomplete_item = {
        "product_name": "Yogurt"
        # Missing brands, price, quantity
    }
    
    response = client.post(
        '/inventory',
        data=json.dumps(incomplete_item),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert data['status'] == 'error'
    assert 'Missing required fields' in data['message']


def test_create_item_empty_body(client, setup_inventory):
    """Test creating an item with empty request body"""
    response = client.post(
        '/inventory',
        data='',
        content_type='application/json'
    )
    
    assert response.status_code == 400


# ===== PATCH ENDPOINT TESTS =====

def test_update_item_success(client, setup_inventory):
    """Test updating an existing item"""
    update_data = {
        "price": 4.99,
        "quantity": 50
    }
    
    response = client.patch(
        '/inventory/1',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['status'] == 'success'
    assert data['data']['price'] == 4.99
    assert data['data']['quantity'] == 50
    # Verify other fields remained unchanged
    assert data['data']['product_name'] == 'Organic Almond Milk'


def test_update_item_partial(client, setup_inventory):
    """Test partial update (update only some fields)"""
    update_data = {
        "quantity": 100
    }
    
    response = client.patch(
        '/inventory/2',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['data']['quantity'] == 100
    assert data['data']['price'] == 2.49  # Unchanged


def test_update_item_not_found(client, setup_inventory):
    """Test updating a non-existent item"""
    update_data = {"price": 5.99}
    
    response = client.patch(
        '/inventory/999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 404
    data = json.loads(response.data)
    
    assert data['status'] == 'error'


# ===== DELETE ENDPOINT TESTS =====

def test_delete_item_success(client, setup_inventory):
    """Test deleting an item"""
    response = client.delete('/inventory/1')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['status'] == 'success'
    assert data['data']['id'] == 1
    
    # Verify item is actually deleted
    verify_response = client.get('/inventory/1')
    assert verify_response.status_code == 404


def test_delete_item_not_found(client, setup_inventory):
    """Test deleting a non-existent item"""
    response = client.delete('/inventory/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    
    assert data['status'] == 'error'


def test_delete_last_item(client, setup_inventory):
    """Test deleting all items"""
    client.delete('/inventory/1')
    client.delete('/inventory/2')
    
    response = client.get('/inventory')
    data = json.loads(response.data)
    
    assert data['count'] == 0
    assert len(data['data']) == 0


# ===== EXTERNAL API ENDPOINT TESTS =====

def test_search_external_api_missing_params(client):
    """Test searching external API without required params"""
    response = client.post(
        '/search-external',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert data['status'] == 'error'
    # Should return error about missing barcode or product_name


def test_search_external_api_empty_body(client):
    """Test searching external API with empty body"""
    response = client.post(
        '/search-external',
        data='',
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_search_external_api_barcode_not_found(client, mocker):
    """Test searching for a barcode that doesn't exist in API"""
    # Mock the requests.get to simulate API response
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"status": 0}
    mocker.patch('requests.get', return_value=mock_response)
    
    response = client.post(
        '/search-external',
        data=json.dumps({"barcode": "9999999999"}),
        content_type='application/json'
    )
    
    assert response.status_code == 500


# ===== HELPER FUNCTION TESTS =====

def test_get_next_id_empty(setup_inventory):
    """Test getting next ID when inventory is empty"""
    inventory.clear()
    next_id = get_next_id()
    
    assert next_id == 1


def test_get_next_id_with_items(setup_inventory):
    """Test getting next ID with items in inventory"""
    next_id = get_next_id()
    
    assert next_id == 3  # After IDs 1 and 2


def test_get_next_id_gap_in_ids(setup_inventory):
    """Test getting next ID when there's a gap in IDs"""
    # Delete item with ID 1, then check next ID
    inventory.pop(0)
    next_id = get_next_id()
    
    # Should still be max + 1
    assert next_id == 3


# ===== ERROR HANDLER TESTS =====

def test_404_error_handler(client):
    """Test 404 error handler"""
    response = client.get('/nonexistent-endpoint')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    
    assert data['status'] == 'error'
    assert 'not found' in data['message'].lower()


def test_405_error_handler(client, setup_inventory):
    """Test 405 error handler (method not allowed)"""
    response = client.put('/inventory')  # PUT not allowed on /inventory
    
    assert response.status_code == 405
    data = json.loads(response.data)
    
    assert data['status'] == 'error'


# ===== INTEGRATION TESTS =====

def test_crud_workflow(client, setup_inventory):
    """Test complete CRUD workflow"""
    
    # Create
    new_item = {
        "product_name": "Test Product",
        "brands": "Test Brand",
        "price": 10.00,
        "quantity": 5
    }
    create_response = client.post(
        '/inventory',
        data=json.dumps(new_item),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    item_id = json.loads(create_response.data)['data']['id']
    
    # Read
    read_response = client.get(f'/inventory/{item_id}')
    assert read_response.status_code == 200
    
    # Update
    update_data = {"price": 12.00}
    update_response = client.patch(
        f'/inventory/{item_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert update_response.status_code == 200
    assert json.loads(update_response.data)['data']['price'] == 12.00
    
    # Delete
    delete_response = client.delete(f'/inventory/{item_id}')
    assert delete_response.status_code == 200
    
    # Verify deleted
    verify_response = client.get(f'/inventory/{item_id}')
    assert verify_response.status_code == 404


def test_multiple_operations(client, setup_inventory):
    """Test multiple operations in sequence"""
    
    # Add multiple items
    for i in range(3):
        client.post(
            '/inventory',
            data=json.dumps({
                "product_name": f"Product {i}",
                "brands": f"Brand {i}",
                "price": 5.00 + i,
                "quantity": 10 + i
            }),
            content_type='application/json'
        )
    
    # Verify count
    response = client.get('/inventory')
    data = json.loads(response.data)
    assert data['count'] == 5  # 2 original + 3 new


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
