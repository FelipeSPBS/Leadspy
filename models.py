from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()  # Mantenha a inicialização do db aqui.

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Pixel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(150), nullable=False)
    pixel_code = db.Column(db.String(100), nullable=False)
    redirect_link = db.Column(db.String(200), nullable=True)
    track_pageview = db.Column(db.Boolean, default=False)
    track_purchase = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
