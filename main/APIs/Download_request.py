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

                                task_path=task.TaskPath
                                task_status=get_task_status_by_path(task_path).Status

                                if task_status!="completed":
                                    # if task_status=="failed":
                                    #     return jsonify({'result': False, 'error_message': f'task not finish yet, current status:{task_status}', 'path': task_path,'task_status':task_status})
                                    # else:
                                    return jsonify({'result': False, 'error_message': f'task not finish yet, current status:{task_status}', 'path': task_path,'task_status':task_status})
                                else:
                                    print(f"{now_time()}: {username} make a successfully Download request")
                                    return jsonify({'result': True, 'error_message': None, 'path': task_path,'task_status':task_status})
                                
                        return jsonify({'result': False, "error_message": 'Task not exist', 'path': None,'task_status':None})
                    

                        # if task_name in tasks:
                        #     task = ProjectTask.query.filter_by(TaskName=task_name).first()
                        #     if task:
                        #         return jsonify({'result': True, 'error_message': None, 'path': task.TaskPath})
                        #     else:
                        #         return jsonify({'result': False, "error_message": 'Task data retrieval failed', 'path': None})
                        # else:
                        #     return jsonify({'result': False, "error_error_message": 'Task not exist', 'path': None})
                    else:
                        return jsonify({'result': False, "error_message": 'Project not exist', 'path': None,'task_status':None})
                else:
                    return jsonify({'result': False, "error_message": 'User not found', 'path': None,'task_status':None})
            else:
                return jsonify({'result': False, "error_message": 'Token does not exist', 'path': None,'task_status':None})
        
        except SQLAlchemyError as e:
            db.session.rollback()

            print(f"{now_time()}: SQLAlchemyError during download_request: {e}")
            logging.error(f"SQLAlchemyError during download_request: {e}")
            return jsonify({'result': False, "error_message": "Database error. Please try again.", 'path': None,'task_status':None})
        except Exception as e:
            
            print(f"{now_time()}: Error during download_request: {e}")
            logging.error(f"Error during download_request: {e}")
            return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again.", 'path': None,'task_status':None})
