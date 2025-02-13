from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from src.models import BudgetEntry, db

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/', methods=['GET'])
def get_budget():
    """
    Retrieve budget entries for a given category and year.
    
    Query Parameters:
      - category_id: (required) the ID of the category.
      - year: (optional) the year to filter by (defaults to current year).
    
    Response JSON example:
    {
      "category_id": 1,
      "year": 2025,
      "values": {
         "1": 500,
         "2": 500,
         // ...
         "12": 500
      }
    }
    """
    category_id = request.args.get("category_id", type=int)
    year = request.args.get("year", default=datetime.now().year, type=int)
    
    if not category_id:
        return jsonify({"error": "Missing 'category_id' query parameter."}), 400

    try:
        entries = BudgetEntry.query.filter_by(category_id=category_id, year=year).all()
        # Build a dictionary with months as keys and their budget values.
        values = {}
        for entry in entries:
            values[str(entry.monat)] = entry.wert
        return jsonify({
            "category_id": category_id,
            "year": year,
            "values": values
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving budget: {e}")
        return jsonify({"error": "Internal server error"}), 500

@budgets_bp.route('/', methods=['POST'])
def save_budget():
    """
    Save or update budget values for a given category and year.
    
    Expected JSON:
      {
          "category_id": 1,
          "year": 2025,              // Optional; defaults to current year if not provided.
          "values": { "1": 500, "2": 500, ..., "12": 500 }
      }
      
    For each month:
      - If an entry exists, update its value.
      - Otherwise, create a new BudgetEntry.
    Uses the SaveMixin's add_instance() method to add to the session and then commits all changes together.
    """
    data = request.get_json()
    category_id = data.get("category_id")
    year = data.get("year", datetime.now().year)
    values = data.get("values")  # Expected: dict with keys "1" through "12"
    
    if not category_id or not values:
        return jsonify({"error": "Invalid data: 'category_id' and 'values' are required."}), 400

    errors = []
    # Process each month separately
    for month, value in values.items():
        try:
            month_int = int(month)
        except ValueError:
            continue  # Skip invalid month keys

        try:
            entry = BudgetEntry.query.filter_by(category_id=category_id, monat=month_int, year=year).first()
            if entry:
                entry.wert = value
                # Add the updated entry to the session (without immediate commit)
                entry.add_instance()
            else:
                new_entry = BudgetEntry(category_id=category_id, monat=month_int, year=year, wert=value)
                new_entry.add_instance()
        except Exception as e:
            current_app.logger.error(f"Error processing month {month}: {e}")
            errors.append(f"Month {month}: {str(e)}")
    
    try:
        # Commit all changes at once
        BudgetEntry.commit_instance()
    except Exception as commit_error:
        current_app.logger.error(f"Error committing changes: {commit_error}")
        return jsonify({"error": "Error committing changes"}), 500

    if errors:
        return jsonify({"error": "Some errors occurred", "details": errors}), 500

    return jsonify({"message": "Budget saved"}), 200