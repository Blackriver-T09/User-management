import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify,flash, current_app
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


from flask import Flask, jsonify, request, abort
from database import db, ProjectTask

class GetAllTaskPaths(views.MethodView):
    def get(self):
        # 确保请求来源是本地
        if request.remote_addr != '127.0.0.1':
            abort(403, description="Access denied: This API is restricted to local access only.")

        try:
            # 获取所有 task 的 path
            tasks = ProjectTask.query.with_entities(ProjectTask.TaskPath).all()
            task_paths = [task.TaskPath for task in tasks]

            return jsonify({"result": True, "task_paths": task_paths})
        
        except Exception as e:
            print(f"Error fetching task paths: {e}")
            return jsonify({"result": False, "error": "An unexpected error occurred."})


