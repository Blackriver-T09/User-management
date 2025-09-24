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
                project = UserProject.query.filter_by(ProjectName=project_name).first()
                if user:
                    if project:
                        print(f"{now_time()}: Project {project_name} exist in the database")
                        return jsonify({'result': True, 'error_message': None})
                    else:    
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