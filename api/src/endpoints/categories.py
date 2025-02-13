# api/src/endpoints/categories.py

from flask import Blueprint, request, jsonify, current_app
from src.models import db, Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
def get_categories():
    """
    Retrieve all categories.
    """
    try:
        categories = Category.query.all()
        return jsonify([cat.as_dict() for cat in categories]), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching categories: {e}")
        return jsonify({"error": "Internal server error"}), 500

@categories_bp.route('', methods=['POST'])
def create_category():
    """
    Create a new category.
    Expected JSON:
      {
          "name": "Category Name",
          "typ": "Einnahme"   // Optional (e.g., "Einnahme" or "Ausgabe")
      }
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Category name is required."}), 400

    try:
        new_cat = Category(name=data['name'], typ=data.get('typ'))
        # Use the SaveMixin's method to add and commit the instance.
        new_cat.save_instance()
        return jsonify(new_cat.as_dict()), 201
    except Exception as e:
        current_app.logger.error(f"Error creating category: {e}")
        return jsonify({"error": "Internal server error"}), 500

@categories_bp.route('/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    """
    Delete a category with the given ID.
    """
    try:
        category = Category.query.get(cat_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting category {cat_id}: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@categories_bp.route('/delete_all', methods=['DELETE'])
def delete_all_categories():
    """
    Delete all categories.
    """
    try:
        categories = Category.query.all()
        for category in categories:
            db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "All categories deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting all categories: {e}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500