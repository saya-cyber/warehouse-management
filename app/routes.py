from flask import Blueprint, request, jsonify
from app import db
from app.models import Product

main = Blueprint("main", __name__)


@main.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200


@main.route('/products', methods=['POST'])
def add_product():
    data = request.get_json() or {}

    name = data.get('name')
    description = data.get('description', '')
    quantity = data.get('quantity', 0)
    price = data.get('price', 0)

    if not name or not name.strip():
        return jsonify({'error': 'Product name is required'}), 400

    try:
        quantity = int(quantity)
        price = float(price)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity or price'}), 400

    if quantity < 0 or price < 0:
        return jsonify({'error': 'Quantity and price cannot be negative'}), 400

    product = Product(name=name.strip(), description=description, quantity=quantity, price=price)
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@main.route('/products/search', methods=['GET'])
def search_products():
    name = request.args.get('name', '').strip()

    if not name:
        return jsonify({'error': 'Search name is required'}), 400

    products = Product.query.filter(Product.name.ilike(f'%{name}%')).all()
    return jsonify([product.to_dict() for product in products]), 200


@main.route('/products/<int:product_id>/receive', methods=['POST'])
def receive_stock(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}

    try:
        amount = int(data.get('quantity', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity'}), 400

    if amount <= 0:
        return jsonify({'error': 'Received quantity must be positive'}), 400

    product.quantity += amount
    db.session.commit()

    return jsonify({'message': 'Stock received successfully', 'product': product.to_dict()}), 200


@main.route('/products/<int:product_id>/issue', methods=['POST'])
def issue_stock(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}

    try:
        amount = int(data.get('quantity', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity'}), 400

    if amount <= 0:
        return jsonify({'error': 'Issued quantity must be positive'}), 400

    if amount > product.quantity:
        return jsonify({'error': 'Insufficient stock'}), 400

    product.quantity -= amount
    db.session.commit()

    return jsonify({'message': 'Stock issued successfully', 'product': product.to_dict()}), 200


@main.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify(product.to_dict()), 200


@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200
