from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    typ = db.Column(db.String(50))  # z.B. "Einnahme" oder "Ausgabe"

    def as_dict(self):
        return {"id": self.id, "name": self.name, "typ": self.typ}

class BudgetEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    monat = db.Column(db.Integer, nullable=False)  # 1 bis 12
    wert = db.Column(db.Float, default=0)
    category = db.relationship("Category", backref="budgets")

    def as_dict(self):
        return {"id": self.id, "category_id": self.category_id, "monat": self.monat, "wert": self.wert}