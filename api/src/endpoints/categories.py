from flask import Blueprint, request, jsonify, current_app
from src.models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([cat.as_dict() for cat in categories]), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching categories: {e}")
        return jsonify({"error": "Internal server error"}), 500

@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Category name is required."}), 400
    try:
        new_cat = Category(name=data['name'], typ=data.get('typ'))
        new_cat.save_instance()  # Using the instance method to add and commit.
        return jsonify(new_cat.as_dict()), 201
    except Exception as e:
        current_app.logger.error(f"Error creating category: {e}")
        return jsonify({"error": "Internal server error"}), 500