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






# 本地API—— Download-request
class Download_request(views.MethodView):
    def get(self):
        token = request.args.get('token')
        project_name = request.args.get('project_name')
        task_name = request.args.get('task_name')

        # 检查请求来源是否是本地
        if request.remote_addr != '127.0.0.1':
            abort(403)  # 403错误：权限不足

        try:
            if check_token_exists(token):
                username = get_username_by_token(token)
                if username:
                    projects = get_projects_by_username(username)

                    if project_name in projects:
                        user_id=get_user_id_by_token(token)
                        tasks = get_tasks_by_project(user_id,project_name)


                        for task in tasks[::-1]:
                            if task.TaskName == task_name:


                                print(f"{now_time()}: {username} successfully Download request")
                                return jsonify({'result': True, 'error_message': None, 'path': task.TaskPath})
                        return jsonify({'result': False, "error_error_message": 'Task not exist', 'path': None})
                    

                        # if task_name in tasks:
                        #     task = ProjectTask.query.filter_by(TaskName=task_name).first()
                        #     if task:
                        #         return jsonify({'result': True, 'error_message': None, 'path': task.TaskPath})
                        #     else:
                        #         return jsonify({'result': False, "error_message": 'Task data retrieval failed', 'path': None})
                        # else:
                        #     return jsonify({'result': False, "error_error_message": 'Task not exist', 'path': None})
                    else:
                        return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
                else:
                    return jsonify({'result': False, "error_message": 'User not found', 'path': None})
            else:
                return jsonify({'result': False, "error_message": 'Token does not exist', 'path': None})
        
        except SQLAlchemyError as e:
            db.session.rollback()

            print(f"{now_time()}: SQLAlchemyError during download_request: {e}")
            logging.error(f"SQLAlchemyError during download_request: {e}")
            return jsonify({'result': False, "error_message": "Database error. Please try again.", 'path': None})
        except Exception as e:
            
            print(f"{now_time()}: Error during download_request: {e}")
            logging.error(f"Error during download_request: {e}")
            return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again.", 'path': None})
