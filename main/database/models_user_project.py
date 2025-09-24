from .config import db


class UserProject(db.Model):
    __tablename__ = 'user_projects'
    UserProjectId = db.Column(db.Integer, primary_key=True)
    ProjectName = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.UserId'))