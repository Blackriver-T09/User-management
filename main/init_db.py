from app import app, db  
from database import *


def init_tables():
    print("Are you sure you want to initialize the database? All data except for backup data will be irreversibly deleted!")
    choice=input("choice(n/y):")
    if choice=='n':
        print('')
    else:
        with app.app_context(): 
            db.drop_all()  
            db.create_all() 
            print("数据库表初始化完成。")



if __name__ == '__main__':
    init_tables()
