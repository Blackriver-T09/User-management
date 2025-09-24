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






class Delete_project(views.MethodView):
    def post(self):
        data = request.get_json()
        token = data.get("token")
        project_name = data.get("project_name")

        if not token or not project_name:
            return jsonify({"result": False, "message": "Please provide token and project name."})

        try:
            user = get_user_by_token(token)
            if not user:
                return jsonify({"result": False, "message": "Invalid token or user not found."})

            # 查找project
            project = UserProject.query.filter_by(user_id=user.UserId, ProjectName=project_name).first()
            if not project:
                return jsonify({"result": False, "message": f"Project '{project_name}' does not exist."})

            # 查找与project关联的task
            tasks = ProjectTask.query.filter_by(user_project_id=project.UserProjectId).all()
            for task in tasks:
                task_status = TaskStatus.query.filter_by(TaskPath=task.TaskPath).first()
                if task_status:
                    db.session.delete(task_status)
                task_time = TaskTime.query.filter_by(TaskPath=task.TaskPath).first()
                if task_time:
                    db.session.delete(task_time)
                db.session.delete(task)                 # 删除任务
                db.session.flush()                   # 确保删除操作立即应用于数据库
                delete_task_request(task.TaskPath)   # 异步通知其他服务器删除任务路径（可选）
            db.session.commit()

            # 删除project
            db.session.delete(project)
            db.session.commit()

            print(f"{now_time()}: Project '{project_name}' and its tasks were successfully deleted by {user.Username}.")
            return jsonify({"result": True, "message": f"Project '{project_name}' deleted successfully."})



        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"{now_time()}: SQLAlchemyError during project deletion: {e}")
            return jsonify({"result": False, "message": "Database error occurred. Please try again later."})
        except Exception as e:
            print(f"{now_time()}: Error during project deletion: {e}")
            return jsonify({"result": False, "message": "An unexpected error occurred. Please try again."})





