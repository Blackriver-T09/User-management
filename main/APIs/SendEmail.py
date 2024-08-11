import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


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

from services.database_operations import check_user_exists, check_token_exists, check_project_exists, check_task_exists, get_token_by_username, get_username_by_token, get_user_by_token, get_level_by_token, get_password_by_username, get_user_info_by_username, get_projects_by_username, get_tasks_by_project, get_username_by_tokenTmp,get_user_id_by_token,verify_user_email
from services.scheduler_tasks  import now_time,start_scheduler





class SendEmail(views.MethodView):
    def post(self):
        data=request.get_json()
        email=data.get('email',None)
        username = data.get("username",None)

        #验证缺失模块 
        parameter_list=[email,username]
        for parameter in parameter_list:
            if parameter == None:
                return jsonify({'result': False, 'error': 'please fill in both the email and username'})


        try:
            user_exist = check_user_exists(username)  # 检查用户是否存在
            if user_exist:
                user = User.query.filter_by(Username=username).first()

                if verify_user_email(username, email):

                    # 创建一个 TokenTmp 实例并保存到数据库
                    tokenTmp = tokenTmp_generate()  # 假设 token_generate() 是一个函数来生成一个临时令牌
                    new_token_tmp = TokenTmp(tempToken=tokenTmp, userId=user.UserId)
                    db.session.add(new_token_tmp)
                    db.session.commit()  # 提交数据库会话以保存我们的更改
                    
                    # 构建重置密码的 URL
                    reset_url = url_for('change_password', tokenTmp=tokenTmp, _external=True)
                    # reset_url = 'https://rshub.zju.edu.cn/change-password/' + tokenTmp


                    # 准备邮件内容
                    message = f'Hello {username},\n\nWe received your request to reset your password. Please click the link below to reset your password. This link will expire in 10 minutes:\n{reset_url}\n\nIf you did not request this change, please ignore this email.'


                    try:
                        send_email(email,message,1) 


                        print(f"{now_time()}: change_password email has been sent to {username} ")
                        return jsonify({'result': True, 'error': None})
                    except Exception as e:

                        print(f"{now_time()}: error happened whenn sending email:{e}")
                        logging.error(f"error happened whenn sending email:{e}")
                        return jsonify({'result': False, 'error': f"error happened whenn sending email:{e}"})
                
                else:
                    error="email doesn't match this username"
                    return jsonify({'result': False, 'error': error})
            else:
                error = "User not exist"
                return jsonify({'result': False, 'error': error})

        except SQLAlchemyError as e:
            # flash(f"A database error occurred: {e}", 'error')

            print(f"{now_time()}: SQLAlchemyError during Email: {e}")
            logging.error(f"SQLAlchemyError during Email: {e}")
            return jsonify({'result': False, 'error': "An internal error occurred. Please try again."})
        except Exception as e:
            # flash(f"An unexpected error occurred: {e}", 'error')

            print(f"{now_time()}: Error during Email: {e}")
            logging.error(f"Error during Email: {e}")
            return jsonify({'result': False, 'error': "An unexpected error occurred. Please try again."})