import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify,flash
from utils import *

from database import *
import os
import logging
import time

from flask_cors import CORS,cross_origin

# 增强容错机制
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from services import *




class Login(views.MethodView):


    def post(self):
        data = request.get_json()
        username = data.get("username",None)
        password = data.get("password",None)
        
        # 验证缺失模块
        parameter_list=[username, password]
        for parameter in parameter_list:
            if parameter == None:
                return jsonify({'result': False, 'error': 'please fill in username and password', 'tokenTmp': None})


        try:
            
            user_exist = check_user_exists(username)  # 检查用户是否存在
            if user_exist:
                user = User.query.filter_by(Username=username).first()
                password_hashed = get_password_by_username(username)
                if decryptor_check(password, password_hashed):  # 验证密码

                    if user.Activated == True:
                        tokenTmp = tokenTmp_generate()  # 生成一个临时令牌

                        # 创建一个 TokenTmp 实例并保存到数据库
                        new_token_tmp = TokenTmp(tempToken=tokenTmp, userId=user.UserId)
                        db.session.add(new_token_tmp)
                        db.session.commit()  # 提交数据库会话以保存我们的更改

                        print(f"{now_time()}: {username} has successfully log in")
                        return jsonify({'result': True, 'error': None, 'tokenTmp': tokenTmp})
                    else:
                        error = "Account not activated!"
                        return jsonify({'result': False, 'error': error, 'tokenTmp': None})
                else:
                    error = "wrong password"
                    return jsonify({'result': False, 'error': error, 'tokenTmp': None})
            else:
                error = "User not exist"
                return jsonify({'result': False, 'error': error, 'tokenTmp': None})


        except SQLAlchemyError as e:
            # flash(f"A database error occurred: {e}", 'error')
            print(f"{now_time()}: SQLAlchemyError during Login: {e}")
            logging.error(f"SQLAlchemyError during Login: {e}")

            return jsonify({'result': False, 'error': "An internal error occurred. Please try again.", 'tokenTmp': None})
        except Exception as e:
            # flash(f"An unexpected error occurred: {e}", 'error')

            print(f"{now_time()}: Error during Login: {e}")
            logging.error(f"Error during Login: {e}")
            return jsonify({'result': False, 'error': "An unexpected error occurred. Please try again.", 'tokenTmp': None})