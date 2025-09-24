from .config import db
from datetime import datetime, timezone


class TaskTime(db.Model):
    __tablename__ = 'task_times'

    TimeId = db.Column(db.Integer, primary_key=True)
    TaskPath = db.Column(db.String(100), db.ForeignKey('project_tasks.TaskPath'), unique=True, nullable=False)
    StartTime = db.Column(db.DateTime, nullable=False, default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    EndTime = db.Column(db.DateTime, nullable=True)  # 结束时间可为空，表示任务可能还在进行中

    # 关系：使得从 ProjectTask 访问其时间记录变得可能
    task = db.relationship('ProjectTask', backref=db.backref('times', uselist=False))

