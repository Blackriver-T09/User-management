from .config import db

class User(db.Model):
    __tablename__ = 'users'
    UserId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Organization = db.Column(db.String(50))
