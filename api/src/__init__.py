# api/src/__init__.py

from flask import Flask # type: ignore
from flask_cors import CORS # type: ignore
from flask_migrate import Migrate # type: ignore
from .models import db
from .endpoints.categories import categories_bp
from .endpoints.budgets import budgets_bp

def create_app(config_object=None):
    app = Flask(__name__)
    
    # Load configuration (either from an external object or defaults)
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user:password@db:3306/mydatabase"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
    
    # Initialize the database and migration support
    db.init_app(app)
    Migrate(app, db)
    
    # Register Blueprints for the endpoints
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(budgets_bp, url_prefix='/api/budgets')
    
    return app