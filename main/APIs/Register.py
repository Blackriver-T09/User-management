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
            if check_user_exists(username):
                return jsonify({'result':False,'error':"User already exist"})
            if check_email_exists(email):
                return jsonify({'result':False,'error':"Email already used"})
                

            # 创建用户信息  
            encrypted_password = hash_encipher(password)
            user = User(Username=username, 
                        Password=encrypted_password, 
                        Email=email, 
                        Organization=institution,
                        FirstName=FirstName,
                        LastName=LastName,
                        Gender=Gender,
                        Country=Country,
                        Affiliation=Affiliation,
                        ResearchArea=ResearchArea,
                        Credits=100)
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

