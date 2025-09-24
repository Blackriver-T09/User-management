from .config import db
from datetime import datetime, timezone



class User(db.Model):
    __tablename__ = 'users'
    UserId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Organization = db.Column(db.String(50))
    
    FirstName = db.Column(db.String(50), nullable=True)  # 可以为空，因为不是所有系统都要求有名字
    LastName = db.Column(db.String(50), nullable=True)
    Gender = db.Column(db.String(10), nullable=True)  # 通常足够存储 'Male', 'Female', 'Other'
    Country = db.Column(db.String(50), nullable=True)
    Affiliation = db.Column(db.String(100), nullable=True)  # 归属，如学校、公司等
    ResearchArea = db.Column(db.String(100), nullable=True)  # 研究领域
    Credits = db.Column(db.Integer, default=100)  # 积分或信誉分，初值设为100

    Activated = db.Column(db.Boolean, default=False, nullable=False)  # 默认为False，表示账户未激活
    createdAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)