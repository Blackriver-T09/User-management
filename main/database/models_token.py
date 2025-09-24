from .config import db


class Token(db.Model):
    __tablename__ = 'tokens'
    TokenId = db.Column(db.Integer, primary_key=True)
    Token = db.Column(db.String(50), nullable=False)
    Level = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.UserId'))