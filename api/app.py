"""
Flask API für das Budget-Projekt

API-Endpunkte:
  GET  /api/categories   - Alle Kategorien abrufen
  POST /api/categories   - Eine neue Kategorie erstellen
  POST /api/budgets      - Budgetwerte für eine Kategorie speichern

Hinweis: Intern läuft der Flask-Server auf Port 5000.
Nach Port-Mapping (in docker-compose) ist die API über http://localhost:5500 erreichbar.
"""

from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS  # type: ignore # Importiere flask-cors
from models import db, Category, BudgetEntry

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user:password@db:3306/mydatabase"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Alle vorhandenen Budget-Kategorien abrufen.
    """
    categories = Category.query.all()
    return jsonify([cat.as_dict() for cat in categories]), 200

@app.route('/api/categories', methods=['POST'])
def create_category():
    """
    Eine neue Kategorie erstellen.
    Erwartete JSON-Daten:
      {
          "name": "Kategorie Name",
          "typ": "Einnahme"  // Optional: z. B. "Einnahme" oder "Ausgabe"
      }
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Der Name der Kategorie ist erforderlich."}), 400

    new_cat = Category(name=data['name'], typ=data.get('typ'))
    db.session.add(new_cat)
    db.session.commit()
    return jsonify(new_cat.as_dict()), 201

@app.route('/api/budgets', methods=['POST'])
def save_budget():
    """
    Budgetwerte für eine Kategorie speichern.
    
    Erwartetes JSON-Format:
      {
          "category_id": 1,
          "year": 2025,
          "values": { "1": 500, "2": 500, ..., "12": 500 }
      }
      
    Für jeden Monat wird entweder ein bestehender Eintrag aktualisiert oder ein neuer erstellt.
    """
    data = request.get_json()
    category_id = data.get("category_id")
    values = data.get("values")  # Erwartet ein Dictionary: { "1": 500, "2": 500, ... }

    if not category_id or not values:
        return jsonify({"error": "Ungültige Daten: 'category_id' und 'values' werden benötigt."}), 400

    for monat, wert in values.items():
        try:
            monat_int = int(monat)
        except ValueError:
            continue  # Überspringe ungültige Monatswerte
        entry = BudgetEntry.query.filter_by(category_id=category_id, monat=monat_int).first()
        if entry:
            entry.wert = wert
        else:
            entry = BudgetEntry(category_id=category_id, monat=monat_int, wert=wert)
            db.session.add(entry)

    db.session.commit()
    return jsonify({"message": "Budget gespeichert"}), 200

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=True)