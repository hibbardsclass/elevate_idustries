from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    cte_program = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'