# api/src/models.py

from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime

db = SQLAlchemy()

class SaveMixin:
    def save_instance(self):
        """
        Adds this instance to the session and commits the transaction immediately.
        """
        self.add_instance()
        self.commit_instance()

    def add_instance(self):
        """
        Adds this instance to the session without committing.
        Use this when you want to batch several additions or updates together.
        """
        db.session.add(self)

    @staticmethod
    def commit_instance():
        """
        Commits the current session.
        If an error occurs, rolls back the session and re-raises the exception.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

# Your models continue as before...

class Category(SaveMixin, db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    typ = db.Column(db.String(50))  # e.g., "Einnahme" or "Ausgabe"
    
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "typ": self.typ
        }

class BudgetEntry(SaveMixin, db.Model):
    __tablename__ = 'budget_entry'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False, default=datetime.now().year)
    monat = db.Column(db.Integer, nullable=False)  # 1 to 12
    wert = db.Column(db.Float, default=0)
    
    # Relationship to Category
    category = db.relationship("Category", backref="budget_entries")
    
    def as_dict(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "year": self.year,
            "monat": self.monat,
            "wert": self.wert
        }

class Transaction(SaveMixin, db.Model):
    __tablename__ = 'transaction'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    external_id = db.Column(db.String(100), nullable=True)
    
    category = db.relationship("Category", backref="transactions")
    
    def as_dict(self):
        return {
            "id": self.id,
            "transaction_date": self.transaction_date.isoformat(),
            "description": self.description,
            "amount": self.amount,
            "category_id": self.category_id,
            "external_id": self.external_id
        }