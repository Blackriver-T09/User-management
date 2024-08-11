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







class Profile(views.MethodView):

    def post(self):

        data=request.get_json()
        tokenTmp=data.get('tokenTmp',None)
        if tokenTmp==None:
            return jsonify({'result':False,
                            'username':None,
                            'token':None,
                            'email':None,
                            'organization':None,
                            'credits':None,
                            'projectlist':None,

                            'FirstName':None,
                            'LastName':None,
                            'Gender':None,
                            'Country':None,
                            'Affiliation':None,
                            'ResearchArea':None,

                            'error':"failed to get tokenTmp"})


        username=get_username_by_tokenTmp(tokenTmp)


        if username=="token out of date":
            return jsonify({'result':False,
                            'username':None,
                            'token':None,
                            'email':None,
                            'organization':None,
                            'credits':None,
                            'projectlist':None,

                            'FirstName':None,
                            'LastName':None,
                            'Gender':None,
                            'Country':None,
                            'Affiliation':None,
                            'ResearchArea':None,

                            'error':"token out of date"})
        elif username =="user not exist":
            return jsonify({'result':False,
                            'username':None,
                            'token':None,
                            'email':None,
                            'organization':None,
                            'credits':None,
                            'projectlist':None,

                            'FirstName':None,
                            'LastName':None,
                            'Gender':None,
                            'Country':None,
                            'Affiliation':None,
                            'ResearchArea':None,

                            'error':"user not exist"})


        try:
            # 获取要展示的用户基本信息
            basic_info = get_user_info_by_username(username)
            if not basic_info:
                return jsonify({'result':False,
                                'username':None,
                                'token':None,
                                'email':None,
                                'organization':None,
                                'credits':None,
                                'projectlist':None,

                                'FirstName':None,
                                'LastName':None,
                                'Gender':None,
                                'Country':None,
                                'Affiliation':None,
                                'ResearchArea':None,

                                'error':'Failed to retrieve user information.'})
            
            email = basic_info.get('Email', "Not Found")
            token = basic_info.get('Token', "No token")
            organization = basic_info.get('Organization', "Not Found")
            credits=basic_info.get('Credits', "Not Found")

            # 更多详细信息
            FirstName=basic_info.get('FirstName', "Not Found")
            LastName=basic_info.get('LastName', "Not Found")
            Gender=basic_info.get('Gender', "Not Found")
            Country=basic_info.get('Country', "Not Found")
            Affiliation=basic_info.get('Affiliation', "Not Found")
            ResearchArea=basic_info.get('ResearchArea', "Not Found")


            # 获取用户项目列表
            projectlist = get_projects_by_username(username)

            if projectlist is None:  # 处理项目列表可能为空的情况
                projectlist = []
                return jsonify({'result':False,
                                'username':None,
                                'token':None,
                                'email':None,
                                'organization':None,
                                'credits':None,
                                'projectlist':None,

                                'FirstName':None,
                                'LastName':None,
                                'Gender':None,
                                'Country':None,
                                'Affiliation':None,
                                'ResearchArea':None,

                                'error':'Failed to load projects.'})


            print(f"{now_time()}: {username} has successfully visited his/her page")
            return jsonify({'result':True,
                            'username':username,
                            'token':token,
                            'email':email,
                            'organization':organization,
                            'credits':credits,
                            'projectlist':projectlist,

                            'FirstName':FirstName,
                            'LastName':LastName,
                            'Gender':Gender,
                            'Country':Country,
                            'Affiliation':Affiliation,
                            'ResearchArea':ResearchArea,

                            'error':None})

        except SQLAlchemyError as e:

            print(f"{now_time()}: SQLAlchemyError during Profile: {e}")
            logging.error(f"SQLAlchemyError during Profile: {e}")

            return jsonify({'result':False,
                            'username':None,
                            'token':None,
                            'email':None,
                            'organization':None,
                            'credits':None,
                            'projectlist':None,

                            'FirstName':None,
                            'LastName':None,
                            'Gender':None,
                            'Country':None,
                            'Affiliation':None,
                            'ResearchArea':None,

                            'error':"An internal error occurred. Please try again."})