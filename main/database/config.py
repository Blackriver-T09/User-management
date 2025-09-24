from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = "root"
    MYSQL_PASSWORD = 'b9!Sta88kVvCCR7'
    MYSQL_DB = 'rshub'

    # 设置 SQLAlchemy 使用的数据库 URI 和跟踪修改的选项。
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = False

    # JWT 配置
    JWT_SECRET_KEY = 'secret_key'  
    JWT_TOKEN_LOCATION = ['headers']  # 可以选择 ['headers', 'cookies', 'query_string', 'json']
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 访问令牌过期时间，单位为秒

