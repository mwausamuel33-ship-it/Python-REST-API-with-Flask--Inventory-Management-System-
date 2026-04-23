"""
Unit Tests for Inventory Management System
This test suite validates all functionality of the Flask API including:
- CRUD operations (Create, Read, Update, Delete)
- External API integration (OpenFoodFacts)
- Error handling and validation
- Helper functions
"""

import pytest
import json
import unittest.mock as mock
from app import app, inventory, get_next_id


# ============= FIXTURES =============

@pytest.fixture
def client():
    """
    Create a test client for the Flask application
    Enables testing without running the server
    """
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def setup_inventory():
    """
    Setup and teardown fixture for inventory data
    Saves original inventory, clears it, adds test data,
    then restores original after test completes
    """
    original_inventory = inventory.copy()
    
    # Clear and setup test data
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
    
    # Cleanup - restore original inventory
    inventory.clear()
    inventory.extend(original_inventory)


# ============= GET TESTS =============

def test_get_all_inventory(client, setup_inventory):
    """
    Test GET /inventory endpoint
    Should return all items with correct count
    """
    response = client.get('/inventory')
    
    # Check response status code
    assert response.status_code == 200
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify response structure
    assert data['status'] == 'success'
    assert data['count'] == 2
    assert len(data['data']) == 2


def test_get_single_item_success(client, setup_inventory):
    """
    Test GET /inventory/<id> endpoint with valid ID
    Should return the requested item with correct data
    """
    response = client.get('/inventory/1')
    
    # Check response status code
    assert response.status_code == 200
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify correct item was returned
    assert data['status'] == 'success'
    assert data['data']['id'] == 1
    assert data['data']['product_name'] == 'Organic Almond Milk'
    assert data['data']['brands'] == 'Silk'


def test_get_single_item_not_found(client, setup_inventory):
    """
    Test GET /inventory/<id> endpoint with invalid ID
    Should return 404 error when item doesn't exist
    """
    response = client.get('/inventory/999')
    
    # Check response is 404
    assert response.status_code == 404
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify error response
    assert data['status'] == 'error'
    assert 'not found' in data['message']


# ============= POST TESTS =============

def test_create_item_success(client, setup_inventory):
    """
    Test POST /inventory endpoint with valid data
    Should create new item with auto-generated ID and return 201 status
    """
    request_data = {
        "product_name": "Greek Yogurt",
        "brands": "Fage",
        "price": 4.99,
        "quantity": 20,
        "barcode": "5901234123459",
        "ingredients_text": "Milk, cultures"
    }
    
    response = client.post(
        '/inventory',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 201
    
    # Parse JSON response
    response_data = json.loads(response.data)
    
    # Verify item was created correctly
    assert response_data['status'] == 'success'
    assert response_data['data']['product_name'] == 'Greek Yogurt'
    assert response_data['data']['id'] == 3  # Next ID after existing items
    assert response_data['data']['price'] == 4.99


def test_create_item_missing_required_field(client, setup_inventory):
    """
    Test POST /inventory endpoint with missing required field
    Should return 400 Bad Request error
    """
    # Request missing 'brands' field
    request_data = {
        "product_name": "Yogurt"
    }
    
    response = client.post(
        '/inventory',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 400
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify error message
    assert data['status'] == 'error'
    assert 'Missing required fields' in data['message']


def test_create_item_empty_body(client, setup_inventory):
    """
    Test POST /inventory endpoint with empty request body
    Should return 400 Bad Request error
    """
    response = client.post(
        '/inventory',
        data='',
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 400


# ============= PATCH TESTS =============

def test_update_item_success(client, setup_inventory):
    """
    Test PATCH /inventory/<id> endpoint with valid update data
    Should update item and return 200 status
    """
    update_data = {
        "price": 5.99,
        "quantity": 10
    }
    
    response = client.patch(
        '/inventory/1',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 200
    
    # Parse JSON response
    response_data = json.loads(response.data)
    
    # Verify item was updated
    assert response_data['status'] == 'success'
    assert response_data['data']['price'] == 5.99
    assert response_data['data']['quantity'] == 10
    # Original fields should remain unchanged
    assert response_data['data']['product_name'] == 'Organic Almond Milk'


def test_update_item_partial(client, setup_inventory):
    """
    Test PATCH /inventory/<id> endpoint with partial update
    Should update only provided fields, leaving others unchanged
    """
    update_data = {
        "ingredients_text": "New Ingredients"
    }
    
    response = client.patch(
        '/inventory/1',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 200
    
    # Parse JSON response
    response_data = json.loads(response.data)
    
    # Verify partial update worked
    assert response_data['status'] == 'success'
    assert response_data['data']['ingredients_text'] == 'New Ingredients'
    # Other fields should be unchanged
    assert response_data['data']['price'] == 3.99
    assert response_data['data']['quantity'] == 45


def test_update_item_not_found(client, setup_inventory):
    """
    Test PATCH /inventory/<id> endpoint with invalid ID
    Should return 404 error when item doesn't exist
    """
    update_data = {
        "price": 5.99
    }
    
    response = client.patch(
        '/inventory/999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 404
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify error response
    assert data['status'] == 'error'
    assert 'not found' in data['message']


# ============= DELETE TESTS =============

def test_delete_item_success(client, setup_inventory):
    """
    Test DELETE /inventory/<id> endpoint with valid ID
    Should delete item and return 200 status
    """
    response = client.delete('/inventory/1')
    
    # Check response status code
    assert response.status_code == 200
    
    # Parse JSON response
    response_data = json.loads(response.data)
    
    # Verify deletion was successful
    assert response_data['status'] == 'success'
    
    # Verify item is actually deleted by checking count
    check_response = client.get('/inventory')
    check_data = json.loads(check_response.data)
    assert check_data['count'] == 1  # Should have 1 item left


def test_delete_item_not_found(client, setup_inventory):
    """
    Test DELETE /inventory/<id> endpoint with invalid ID
    Should return 404 error when item doesn't exist
    """
    response = client.delete('/inventory/999')
    
    # Check response status code
    assert response.status_code == 404
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify error response
    assert data['status'] == 'error'


# ============= EXTERNAL API TESTS =============

def test_search_external_api_missing_params(client):
    """
    Test POST /search-external endpoint without search parameters
    Should return 400 Bad Request error
    """
    response = client.post(
        '/search-external',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 400


def test_search_external_api_empty_body(client):
    """
    Test POST /search-external endpoint with empty body
    Should return 400 Bad Request error
    """
    response = client.post(
        '/search-external',
        data='',
        content_type='application/json'
    )
    
    # Check response status code
    assert response.status_code == 400


# ============= HELPER FUNCTION TESTS =============

def test_get_next_id_empty(setup_inventory):
    """
    Test get_next_id() function with empty inventory
    Should return 1 when no items exist
    """
    inventory.clear()
    assert get_next_id() == 1


def test_get_next_id_with_items(setup_inventory):
    """
    Test get_next_id() function with existing items
    Should return ID greater than the maximum existing ID
    """
    # Inventory has items with IDs 1 and 2
    assert get_next_id() == 3


# ============= ERROR HANDLER TESTS =============

def test_404_error_handler(client):
    """
    Test 404 error handler for non-existent endpoints
    Should return proper error response
    """
    response = client.get('/nonexistent-endpoint')
    
    # Check response status code
    assert response.status_code == 404
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify error response format
    assert data['status'] == 'error'
    assert 'not found' in data['message'].lower()


def test_405_error_handler(client, setup_inventory):
    """
    Test 405 error handler for invalid HTTP methods
    Should return proper error response
    """
    # GET /inventory endpoint doesn't support PUT method
    response = client.put('/inventory')
    
    # Check response status code
    assert response.status_code == 405
    
    # Parse JSON response
    data = json.loads(response.data)
    
    # Verify error response format
    assert data['status'] == 'error'


# ============= MAIN =============

if __name__ == '__main__':
    # Run all tests with verbose output
    pytest.main([__file__, '-v'])
