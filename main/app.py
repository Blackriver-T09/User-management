from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify,flash
from utils import username_check,password_check,email_check, hash_encipher, decryptor_check,send_email,path_generate,token_generate,tokenTmp_generate


from database.models_user import User
from database.models_token import Token
from database.models_user_project import UserProject
from database.models_project_task import ProjectTask
from database.temp_tokens import TokenTmp
from database.config import Config
from database.config import db


import os
import logging
import time


from flask_cors import CORS,cross_origin

# 增强容错机制
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from services.database_operations import *       #所有的数据库操作函数
from services.scheduler_tasks  import *          #所有的定时任务

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # 设置一个安全的密钥用于签名会话

app.config.from_object(Config)
CORS(app)

db.app=app
db.init_app(app)




# 导入所有API
from APIs.Register import Register 
from APIs.Profile import Profile
from APIs.Login import Login
from APIs.Change_password import Change_password
from APIs.SendEmail import SendEmail

from APIs.Project_creation import Project_creation
from APIs.Task_creation import Task_creation
from APIs.Download_request import Download_request

from APIs.Check_credits import Check_credits
from APIs.Update_credits import Update_credits



# 网页API
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/', view_func=Login.as_view('main_website'))
app.add_url_rule('/profile', view_func=Profile.as_view('profile'))
app.add_url_rule('/register',view_func=Register.as_view('register'))
app.add_url_rule('/change-password/<tokenTmp>', view_func=Change_password.as_view('change_password'), methods=['GET', 'POST'])
app.add_url_rule('/api/email',view_func=SendEmail.as_view('send_email'))

# 本地API
app.add_url_rule('/api/Project-creation',view_func=Project_creation.as_view('project_creation'))
app.add_url_rule('/api/Task-creation',view_func=Task_creation.as_view('task_creation'))
app.add_url_rule('/api/Download-request',view_func=Download_request.as_view('download_request'))

# 
app.add_url_rule('/api/Check-credits',view_func=Check_credits.as_view('check_credits'))
app.add_url_rule('/api/Update-credits',view_func=Update_credits.as_view('update_credits'))



# 错误处理模块
@app.errorhandler(404)
def handle_404_error(err):
    # return "发生了错误，错误情况是：%s"%err
    return render_template('404.html')
@app.errorhandler(403)
def handle_404_error(err):
    # return "发生了错误，错误情况是：%s"%err
    return render_template('403.html')




if __name__ == '__main__':

    

    # 配置日志
    logging.basicConfig(filename='./log/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
    file_handler = logging.FileHandler('./log/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 配置日志处理器
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # 调整SQLAlchemy的日志级别
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.WARNING)






    #设置定时任务
    gap_hours=24  #设置备份间隔时间
    reserve_folder_path= os.path.join(os.path.dirname(__file__), 'reserved')   #获取备份文件夹目录
    start_scheduler(app,db,reserve_folder_path,gap_hours)    #定时任务启动，每十分钟删除一次过期tokenTmp

    app.run(debug=True)






