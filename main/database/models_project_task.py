from .config import db



class ProjectTask(db.Model):
    __tablename__ = 'project_tasks'
    ProjectTaskId = db.Column(db.Integer, primary_key=True)
    TaskName = db.Column(db.String(50), nullable=False)
    TaskPath = db.Column(db.String(100), nullable=False, unique=True, index=True)  
    user_project_id = db.Column(db.Integer, db.ForeignKey('user_projects.UserProjectId'))
