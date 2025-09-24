# 增加上级路径
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))



from flask import Flask

from database.models_user import User
from database.models_token import Token
from database.models_user_project import UserProject
from database.models_project_task import ProjectTask
from database.config import Config
from database.config import db



app = Flask(__name__) 

app.config.from_object(Config)


db.app=app
db.init_app(app)

def check_user_exists(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        return True  # 用户存在
    return False  # 用户不存在
def get_token_by_username(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        token = Token.query.filter_by(user_id=user.UserId).first()
        if token:
            return token.Token
    return None
def get_level_by_token(token_value):
    token = Token.query.filter_by(Token=token_value).first()
    if token:
        return token.Level
    return None
def get_user_info_by_username(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        token = Token.query.filter_by(user_id=user.UserId).first()
        return {
            "Email": user.Email,
            "Token": token.Token if token else 'No token',
            "Organization": user.Organization
        }
    return None
def get_projects_by_username(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        projects = UserProject.query.filter_by(user_id=user.UserId).all()
        return [project.ProjectName for project in projects]
    return None





# 记录用户信息和项目信息
@app.route('/')
def record_user_and_project():
    # 创建用户信息
    user = User(Username='Student', Password='1234', Email='123@qq.com', Organization=None)
    db.session.add(user)
    db.session.commit()

    # 创建令牌信息
    token = Token(Token='qwer', Level=1, user_id=user.UserId)
    db.session.add(token)
    db.session.commit()

    # 创建项目信息
    project = UserProject(ProjectName='Math', user_id=user.UserId)
    db.session.add(project)
    db.session.commit()

    # 创建任务信息
    task1 = ProjectTask(TaskName='task1', TaskPath='12345', user_project_id=project.UserProjectId)
    task2 = ProjectTask(TaskName='task2', TaskPath='67890', user_project_id=project.UserProjectId)
    db.session.add_all([task1, task2])
    db.session.commit()

    return "User and project information recorded successfully!"


@app.route('/test')
def test():
    content=[check_user_exists('Student'),
            get_token_by_username('Student'),
            get_level_by_token('qwer'),
            get_user_info_by_username('Student'),
            get_projects_by_username('Student')]
    
    return content



if __name__ == '__main__':
    with app.app_context():  #创建临时的Flask应用上下文
        
        db.drop_all()  # 删除数据库下的所有 上述定义 的表，防止重复创建
        db.create_all()  # 将上述定义的所有表对象映射为数据库下的表单（创建表）
    app.run(debug=True)


