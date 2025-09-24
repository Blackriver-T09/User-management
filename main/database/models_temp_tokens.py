from .config import db
from datetime import datetime, timezone




class TokenTmp(db.Model):
    __tablename__ = 'tokenTmp'

    tokenid = db.Column(db.Integer, primary_key=True)
    tempToken = db.Column(db.String(255), nullable=False, unique=True)
    createdAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 使用带 UTC 时区的 now 方法
    userId = db.Column(db.Integer, db.ForeignKey('users.UserId'))

    # 关系：这将在查询用户时启用反向引用，从而可以访问与特定用户关联的令牌
    user = db.relationship('User', backref=db.backref('tokensTmp', lazy=True))






