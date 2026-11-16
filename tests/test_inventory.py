import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite://'})
    with app.app_context():
        db.create_all()
        with app.test_client() as test_client:
            yield test_client
        db.session.remove()
        db.drop_all()

def test_add_product(client):
    response = client.post('/products', json={'name': 'Test Laptop', 'quantity': 10, 'price': 250000})
    assert response.status_code == 201
    assert response.get_json()['name'] == 'Test Laptop'
    assert response.get_json()['quantity'] == 10

def test_receive_stock(client):
    product = Product(name='Test Laptop', quantity=10, price=250000)
    db.session.add(product)
    db.session.commit()
    response = client.post(f'/products/{product.id}/receive', json={'quantity': 5})
    assert response.status_code == 200
    assert response.get_json()['product']['quantity'] == 15

def test_issue_stock(client):
    product = Product(name='Test Laptop', quantity=10, price=250000)
    db.session.add(product)
    db.session.commit()
    response = client.post(f'/products/{product.id}/issue', json={'quantity': 3})
    assert response.status_code == 200
    assert response.get_json()['product']['quantity'] == 7

def test_issue_more_than_available(client):
    product = Product(name='Test Laptop', quantity=10, price=250000)
    db.session.add(product)
    db.session.commit()
    response = client.post(f'/products/{product.id}/issue', json={'quantity': 20})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Insufficient stock'
    assert product.quantity == 10
