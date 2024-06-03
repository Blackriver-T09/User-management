from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = "Your username"
    MYSQL_PASSWORD = 'Your Password'
    MYSQL_DB = 'user_management'

    # 设置 SQLAlchemy 使用的数据库 URI 和跟踪修改的选项。
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


