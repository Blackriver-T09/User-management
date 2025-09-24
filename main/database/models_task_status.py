from .config import db

from datetime import datetime, timezone


class TaskStatus(db.Model):
    __tablename__ = 'task_status'
    
    StatusId = db.Column(db.Integer, primary_key=True)
    TaskPath = db.Column(db.String(100), db.ForeignKey('project_tasks.TaskPath'), unique=True, nullable=False)
    Status = db.Column(db.String(50), nullable=False, default='in queue')
    UpdatedAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # 关系：使得从 ProjectTask 访问其状态变得可能
    task = db.relationship('ProjectTask', backref=db.backref('status', uselist=False))

    
