import pytest
from app import app, db
from models import Hero, Power, HeroPower
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_hero(client):
    response = client.post('/heroes', json={'name': 'Test Hero', 'super_name': 'Test Super'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Hero'
    assert data['super_name'] == 'Test Super'

def test_get_heroes(client):
    client.post('/heroes', json={'name': 'Test Hero', 'super_name': 'Test Super'})
    response = client.get('/heroes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1

def test_get_hero_not_found(client):
    response = client.get('/heroes/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_delete_hero(client):
    post_resp = client.post('/heroes', json={'name': 'Delete Hero', 'super_name': 'Delete Super'})
    hero_id = post_resp.get_json()['id']
    del_resp = client.delete(f'/heroes/{hero_id}')
    assert del_resp.status_code == 204
    get_resp = client.get(f'/heroes/{hero_id}')
    assert get_resp.status_code == 404

def test_create_power(client):
    response = client.post('/powers', json={'name': 'Test Power', 'description': 'This is a test power description'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Power'

def test_update_power(client):
    post_resp = client.post('/powers', json={'name': 'Update Power', 'description': 'Initial description with enough length'})
    power_id = post_resp.get_json()['id']
    patch_resp = client.patch(f'/powers/{power_id}', json={'description': 'Updated description with enough length'})
    assert patch_resp.status_code == 200
    data = patch_resp.get_json()
    assert data['description'] == 'Updated description with enough length'

def test_delete_power(client):
    post_resp = client.post('/powers', json={'name': 'Delete Power', 'description': 'Description for delete power'})
    power_id = post_resp.get_json()['id']
    del_resp = client.delete(f'/powers/{power_id}')
    assert del_resp.status_code == 204
    get_resp = client.get(f'/powers/{power_id}')
    assert get_resp.status_code == 404

def test_create_hero_power(client):
    hero_resp = client.post('/heroes', json={'name': 'HP Hero', 'super_name': 'HP Super'})
    power_resp = client.post('/powers', json={'name': 'HP Power', 'description': 'Description for HP power'})
    hero_id = hero_resp.get_json()['id']
    power_id = power_resp.get_json()['id']
    hp_resp = client.post('/hero_powers', json={'strength': 'Strong', 'hero_id': hero_id, 'power_id': power_id})
    assert hp_resp.status_code == 201
    data = hp_resp.get_json()
    assert data['strength'] == 'Strong'
    assert data['hero_id'] == hero_id
    assert data['power_id'] == power_id

def test_create_hero_power_missing_fields(client):
    response = client.post('/hero_powers', json={'strength': 'Strong'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data
