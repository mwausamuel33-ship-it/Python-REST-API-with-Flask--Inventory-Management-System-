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


# === External API Tests ===

def test_search_external_api_missing_params(client):
    r=client.post('/search-external',data=json.dumps({}),content_type='application/json')
    assert r.status_code==400
    d=json.loads(r.data)
    assert d['status']=='error'


def test_search_external_api_empty_body(client):
    r=client.post('/search-external',data='',content_type='application/json')
    assert r.status_code==400


# === Helper Function Tests ===

def test_get_next_id_empty(setup_inventory):
    inventory.clear()
    assert get_next_id()==1


def test_get_next_id_with_items(setup_inventory):
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


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
