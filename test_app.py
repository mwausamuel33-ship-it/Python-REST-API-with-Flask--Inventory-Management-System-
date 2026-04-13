"""Test module for inventory management API.

Tests Flask endpoints and external API integration.
"""

import pytest
import json
import sys
import unittest.mock as mock
from app import app, inventory, get_next_id


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def setup_inventory():
    original = inventory.copy()
    inventory.clear()
    inventory.extend([
        {"id":1,"product_name":"Organic Almond Milk","brands":"Silk","barcode":"5901234123457","price":3.99,"quantity":45,"ingredients_text":"Filtered water, almonds, cane sugar","created_at":"2024-01-15"},
        {"id":2,"product_name":"Whole Wheat Bread","brands":"Nature's Best","barcode":"5901234123458","price":2.49,"quantity":30,"ingredients_text":"Whole wheat flour, water, yeast","created_at":"2024-01-20"}
    ])
    yield
    inventory.clear()
    inventory.extend(original)


# === GET Tests ===

def test_get_all_inventory(client,setup_inventory):
    r=client.get('/inventory')
    assert r.status_code==200
    d=json.loads(r.data)
    assert d['status']=='success' and d['count']==2 and len(d['data'])==2


def test_get_single_item_success(client,setup_inventory):
    r=client.get('/inventory/1')
    assert r.status_code==200
    d=json.loads(r.data)
    assert d['status']=='success' and d['data']['id']==1 and d['data']['product_name']=='Organic Almond Milk'


def test_get_single_item_not_found(client,setup_inventory):
    r=client.get('/inventory/999')
    assert r.status_code==404
    d=json.loads(r.data)
    assert d['status']=='error' and 'not found' in d['message']


# === POST Tests ===

def test_create_item_success(client,setup_inventory):
    d={"product_name":"Greek Yogurt","brands":"Fage","price":4.99,"quantity":20,"barcode":"5901234123459","ingredients_text":"Milk, cultures"}
    r=client.post('/inventory',data=json.dumps(d),content_type='application/json')
    assert r.status_code==201
    t=json.loads(r.data)
    assert t['status']=='success' and t['data']['product_name']=='Greek Yogurt' and t['data']['id']==3


def test_create_item_missing_required_field(client,setup_inventory):
    r=client.post('/inventory',data=json.dumps({"product_name":"Yogurt"}),content_type='application/json')
    assert r.status_code==400
    d=json.loads(r.data)
    assert d['status']=='error' and 'Missing required fields' in d['message']


def test_create_item_empty_body(client,setup_inventory):
    r=client.post('/inventory',data='',content_type='application/json')
    assert r.status_code==400


# === PATCH Tests ===

def test_update_item_success(client,setup_inventory):
    d={"price":4.99,"quantity":50}
    r=client.patch('/inventory/1',data=json.dumps(d),content_type='application/json')
    assert r.status_code==200
    t=json.loads(r.data)
    assert t['status']=='success' and t['data']['price']==4.99 and t['data']['quantity']==50 and t['data']['product_name']=='Organic Almond Milk'


def test_update_item_partial(client,setup_inventory):
    d={"quantity":100}
    r=client.patch('/inventory/2',data=json.dumps(d),content_type='application/json')
    assert r.status_code==200
    t=json.loads(r.data)
    assert t['data']['quantity']==100 and t['data']['price']==2.49


def test_update_item_not_found(client,setup_inventory):
    r=client.patch('/inventory/999',data=json.dumps({"price":5.99}),content_type='application/json')
    assert r.status_code==404
    d=json.loads(r.data)
    assert d['status']=='error'


# === DELETE Tests ===

def test_delete_item_success(client,setup_inventory):
    r=client.delete('/inventory/1')
    assert r.status_code==200
    d=json.loads(r.data)
    assert d['status']=='success' and d['data']['id']==1
    assert client.get('/inventory/1').status_code==404


def test_delete_item_not_found(client,setup_inventory):
    r=client.delete('/inventory/999')
    assert r.status_code==404
    d=json.loads(r.data)
    assert d['status']=='error'


def test_delete_last_item(client,setup_inventory):
    client.delete('/inventory/1')
    client.delete('/inventory/2')
    r=client.get('/inventory')
    d=json.loads(r.data)
    assert d['count']==0 and len(d['data'])==0


# === External API Tests ===

def test_search_external_api_missing_params(client):
    r=client.post('/search-external',data=json.dumps({}),content_type='application/json')
    assert r.status_code==400
    d=json.loads(r.data)
    assert d['status']=='error'


def test_search_external_api_empty_body(client):
    r=client.post('/search-external',data='',content_type='application/json')
    assert r.status_code==400


def test_search_external_api_barcode_not_found(client):
    """Test searching for a barcode that doesn't exist in API"""
    with mock.patch('app.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": 0}
        response = client.post(
            '/search-external',
            data=json.dumps({"barcode": "9999999999"}),
            content_type='application/json'
        )
        assert response.status_code == 500


# === Helper Function Tests ===

def test_get_next_id_empty(setup_inventory):
    inventory.clear()
    assert get_next_id()==1


def test_get_next_id_with_items(setup_inventory):
    assert get_next_id()==3


def test_get_next_id_gap_in_ids(setup_inventory):
    inventory.pop(0)
    assert get_next_id()==3


# === Error Handler Tests ===

def test_404_error_handler(client):
    r=client.get('/nonexistent-endpoint')
    assert r.status_code==404
    d=json.loads(r.data)
    assert d['status']=='error' and 'not found' in d['message'].lower()


def test_405_error_handler(client,setup_inventory):
    r=client.put('/inventory')
    assert r.status_code==405
    d=json.loads(r.data)
    assert d['status']=='error'


# === Integration Tests ===

def test_crud_workflow(client,setup_inventory):
    # Create
    it={"product_name":"Test Product","brands":"Test Brand","price":10.00,"quantity":5}
    r=client.post('/inventory',data=json.dumps(it),content_type='application/json')
    assert r.status_code==201
    id=json.loads(r.data)['data']['id']
    # Read
    assert client.get(f'/inventory/{id}').status_code==200
    # Update
    r=client.patch(f'/inventory/{id}',data=json.dumps({"price":12.00}),content_type='application/json')
    assert json.loads(r.data)['data']['price']==12.00
    # Delete
    assert client.delete(f'/inventory/{id}').status_code==200
    assert client.get(f'/inventory/{id}').status_code==404


def test_multiple_operations(client,setup_inventory):
    for i in range(3):
        client.post('/inventory',data=json.dumps({"product_name":f"Product {i}","brands":f"Brand {i}","price":5.00+i,"quantity":10+i}),content_type='application/json')
    r=client.get('/inventory')
    assert json.loads(r.data)['count']==5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
