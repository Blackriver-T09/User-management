from app import app, db  
from database.models_user import User
from database.models_token import Token
from database.models_user_project import UserProject
from database.models_project_task import ProjectTask
from database.temp_tokens import TokenTmp


def init_tables():
    with app.app_context(): 
        db.drop_all()  
        db.create_all() 

if __name__ == '__main__':
    init_tables()
    print("数据库表初始化完成。")
