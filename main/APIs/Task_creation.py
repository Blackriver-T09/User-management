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




# 本地API——Task-creation
class Task_creation(views.MethodView):
    def get():
        token = request.args.get('token')
        project_name = request.args.get('project_name')
        task_name = request.args.get('task_name')
        level_required = request.args.get('level', 1)

        # 检查请求来源是否是本地
        if request.remote_addr != '127.0.0.1':
            abort(403)  # 403错误：权限不足

        try:
            if check_token_exists(token):
                user = get_username_by_token(token)
                projects = get_projects_by_username(user)

                if project_name in projects:
                    level = get_level_by_token(token)
                    
                    if level and int(level) >= int(level_required):
                        # 创建新的任务
                        new_task = ProjectTask(TaskName=task_name, TaskPath=path_generate())

                        # 查询项目并将任务与项目关联
                        project = UserProject.query.filter_by(ProjectName=project_name).first()
                        if project:
                            new_task.user_project_id = project.UserProjectId
                            db.session.add(new_task)
                            db.session.commit()

                            print(f"{now_time()}: {user.Username} successfully create task '{task_name}' in project '{project_name}'")
                            return jsonify({'result': True, 'error_message': None, 'path': new_task.TaskPath})
                        else:
                            return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
                    else:
                        return jsonify({'result': False, "error_message": 'Insufficient permissions', 'path': None})
                else:
                    return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
            else:
                return jsonify({'result': False, "error_message": 'Token does not exist', 'path': None})

        except SQLAlchemyError as e:
            db.session.rollback()

            print(f"{now_time()}: SQLAlchemyError during Task-creation: {e}")
            logging.error(f"SQLAlchemyError during Task-creation: {e}")
            return jsonify({'result': False, "error_message": "Database error. Unable to create task.", 'path': None})
        except Exception as e:

            print(f"{now_time()}: Error during Task-creation: {e}")
            logging.error(f"Error during Task-creation: {e}")
            return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again.", 'path': None})
