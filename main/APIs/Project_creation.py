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



# 本地API——Project-creation     
class Project_creation(views.MethodView):
    def get(self):
        token = request.args.get('token')
        project_name = request.args.get('project_name')

        # 检查请求来源是否是本地
        if request.remote_addr != '127.0.0.1':
            abort(403)  # 403错误：权限不足

        try:
            if check_token_exists(token):
                user = get_user_by_token(token)  # 获取与该token相关联的用户对象
                if user:
                    project = UserProject(ProjectName=project_name, user_id=user.UserId)
                    db.session.add(project)
                    db.session.commit()

                    print(f"{now_time()}: {user.Username} successfully create project {project_name}")
                    return jsonify({'result': True, 'error_message': None})
                else:
                    return jsonify({'result': False, "error_message": 'User not found'})
            else:
                return jsonify({'result': False, "error_message": 'Token does not exist'})

        except SQLAlchemyError as e:
            db.session.rollback()

            print(f"{now_time()}: SQLAlchemyError during project_creation: {e}")
            logging.error(f"SQLAlchemyError during project_creation: {e}")
            return jsonify({'result': False, "error_message": "Database error. Unable to create project."})
        except Exception as e:
            
            print(f"{now_time()}: Error during project_creation: {e}")
            logging.error(f"Error during project_creation: {e}")
            return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again."})