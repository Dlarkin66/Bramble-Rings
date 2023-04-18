from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    materials = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    image_url_2 = db.Column(db.String(200))
    image_url_3= db.Column(db.String(200))
    image_url_4 = db.Column(db.String(200))






