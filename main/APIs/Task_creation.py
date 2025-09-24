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




# 本地API——Task-creation
class Task_creation(views.MethodView):
    def get(self):
        token             = request.args.get('token')
        project_name      = request.args.get('project_name')
        task_name         = request.args.get('task_name')
        level_required    = request.args.get('level', 1)
        force_update_flag = request.args.get('force_update_flag',0)

        # 检查请求来源是否是本地
        if request.remote_addr != '127.0.0.1':
            abort(403)  # 403错误：权限不足

        try:
            if check_token_exists(token):
                user = get_user_by_token(token)
                projects = get_projects_by_username(user.Username)

                if project_name in projects:
                    level = get_level_by_token(token)
                    
                    if level and int(level) >= int(level_required):     

                        #检查是否有重名任务
                        existing_task = ProjectTask.query.filter_by(TaskName=task_name).first()
                        if existing_task:
                            if int(force_update_flag) == 1:
                                # 删除重名任务及相关信息
                                task_status = TaskStatus.query.filter_by(TaskPath=existing_task.TaskPath).first()
                                if task_status:
                                    db.session.delete(task_status)
                                
                                task_time = TaskTime.query.filter_by(TaskPath=existing_task.TaskPath).first()
                                if task_time:
                                    db.session.delete(task_time)
                                
                                db.session.delete(existing_task)
                                db.session.commit()

                                print(f"{now_time()}: User '{user.Username}' deleted existing task '{task_name}' in project '{project_name}' as force_update_flag=1.")
                            else:
                                return jsonify({'result': False, "error_message": 'Task already exists. Set force_update_flag to 1 to overwrite.', 'path': None})



                        # 创建新的任务
                        new_task = ProjectTask(TaskName=task_name, TaskPath=path_generate())

                        # 查询项目并将任务与项目关联
                        project = UserProject.query.filter_by(ProjectName=project_name).first()
                        if project:
                            new_task.user_project_id = project.UserProjectId
                            db.session.add(new_task)
                            db.session.flush()  # 立即生成 TaskPath

                            # 创建任务状态记录
                            new_task_status = TaskStatus(TaskPath=new_task.TaskPath)
                            db.session.add(new_task_status)
                            db.session.flush()

                            # 创建任务起始时间
                            new_task_status = TaskTime(TaskPath=new_task.TaskPath)
                            db.session.add(new_task_status)                            
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
