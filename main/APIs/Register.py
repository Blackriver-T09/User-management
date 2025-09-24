import sys
import os
from datetime import datetime, timezone, timedelta
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






class Register(views.MethodView):
     # 允许所有域进行跨源请求
    def post(self):

        # 基础信息
        data= request.get_json()
        username = data.get('username',None)
        email = data.get('email',None)
        institution = data.get('institution',None)
        password = data.get('password',None)
        confirm_password = data.get('confirm_password',None)

        # 更详细的信息
        FirstName=data.get('FirstName',None)
        LastName=data.get('LastName',None)
        Gender=data.get('Gender',None)
        Country=data.get('Country',None)
        Affiliation=data.get('Affiliation',None)
        ResearchArea=data.get('ResearchArea',None)

        # 验证缺失模块
        parameter_list=[username,email,institution,password,confirm_password,FirstName,
                        LastName,Gender,Country,Affiliation,ResearchArea]
        for parameter in parameter_list:
            if parameter == None:
                return jsonify({'result':False,'error':f'please fill in ALL the required infomation'})



        # 安全性验证模块
        username_result, username_error = username_check(username)
        email_result, email_error = email_check(email)
        password_result, password_error = password_check(password)
        if not username_result:
            return jsonify({'result':False,'error':username_error})
        if not email_result:
            return jsonify({'result':False,'error':email_error})
        if not password_result:
            return jsonify({'result':False,'error':password_error})
        if password != confirm_password:
            return jsonify({'result':False,'error':"confirm password not match your password!"})


        # 所有验证通过，进行注册
        try:

            # 检查用户是否已经存在。如果存在且未激活，则检查未激活账户的注册时间。30秒内不允许重新注册
            user = User.query.filter_by(Username=username).first()
            if user and not user.Activated:
                if user.createdAt.tzinfo is None: # 确保 user.createdAt 是 offset-aware 的时间
                    created_at = user.createdAt.replace(tzinfo=timezone.utc)
                else:
                    created_at = user.createdAt

                time_diff = datetime.now(timezone.utc) - created_at
                if time_diff.total_seconds() < 30:
                    return jsonify({'result': False, 'error': "An unactivated account already exists. Please wait 30 seconds before retrying."})

            # 检查用户是否已经存在。如果存在但是未激活，则删除已有账号重新注册
            if user:
                if not user.Activated:
                    TokenTmp.query.filter_by(userId=user.UserId).delete()
                    db.session.delete(user)
                    db.session.commit()
                    print(f"{now_time()}: Deleted existing unactivated account for username '{username}'.")
                else:
                    return jsonify({'result': False, 'error': "User already exists and is activated."})
                

            # 检查邮件对应的用户是否已经存在。如果存在但是未激活，则删除已有账号重新注册
            user = User.query.filter_by(Email=email).first()
            if user:
                if not user.Activated:
                    TokenTmp.query.filter_by(userId=user.UserId).delete()
                    db.session.delete(user)
                    db.session.commit()
                    print(f"{now_time()}: Deleted existing unactivated account for username '{username}'.")
                else:
                    return jsonify({'result': False, 'error': "Email already exists and is activated."})
            

                

            # 创建用户信息  
            encrypted_password = hash_encipher(password)
            user = User(
                Username=username, 
                Password=encrypted_password, 
                Email=email, 
                Organization=institution,
                FirstName=FirstName,
                LastName=LastName,
                Gender=Gender,
                Country=Country,
                Affiliation=Affiliation,
                ResearchArea=ResearchArea,
                Credits=100,
                Activated=False,  # 显式设置账户为未激活
                createdAt=datetime.now(timezone.utc)  # 显式设置账户注册时间为当前时间
            )
            db.session.add(user)
            db.session.flush()  # Flush to assign ID to user object without committing transaction



            # 创建临时令牌  并保存到数据库
            tokenTmp = tokenTmp_generate()  
            new_token_tmp = TokenTmp(tempToken=tokenTmp, userId=user.UserId)   #临时令牌实例
            db.session.add(new_token_tmp)
            db.session.commit()  

            activation_link = url_for('activate_account', tokenTmp=tokenTmp, _external=True)

            send_email(email,f'Congratulations,{username}! \n Please click this link {activation_link} to finish the last step to activate your account! ',0)

            print(f'{now_time()}: {username} has completed the preliminary registration task')

            return jsonify({'result':True,'error':None})
        
        except Exception as e:
            db.session.rollback()

            print(f"{now_time()}: Error during registration: {e}")
            logging.error(f"Error during registration: {e}")

            return jsonify({'result':False,'error':"An error occurred during registration. Please try again.",'tokenTmp':None})

