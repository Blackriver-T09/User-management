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

from .config import B_USERNAME,B_PASSWORD,SECRETKEY,MINS
from .tools import *




class DatabaseInfo(views.MethodView):
    def post(self):
        # 从 HTTP 头中获取 token
        token = request.headers.get('Authorization', '').split(" ")[1] if 'Authorization' in request.headers else None
        
        mins = MINS
        key = SECRETKEY

        # 验证 token
        if token and is_token_valid(token, key, mins):
            try:
                user_count = User.query.count()
                project_count = UserProject.query.count()
                task_count = ProjectTask.query.count()
                calculating_tasks = TaskStatus.query.filter_by(Status='calculating').count()
                queued_tasks = TaskStatus.query.filter_by(Status='in queue').count()
                completed_tasks = TaskStatus.query.filter_by(Status='complete').count()

                return jsonify({
                    'user_count': user_count,
                    'project_count': project_count,
                    'task_count': task_count,
                    'calculating_tasks': calculating_tasks,
                    'queued_tasks': queued_tasks,
                    'completed_tasks': completed_tasks
                })
            

            except SQLAlchemyError as e:
                print(f"Database error occurred: {e}")
                return jsonify({'error': 'Database error occurred'}), 500
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return jsonify({'error': 'An unexpected error occurred'}), 500
            

            
        else:
            return jsonify({'error': 'Unauthorized or token expired'}), 401




