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





class Delete_task(views.MethodView):
    def post(self):
        data = request.get_json()

        token = data.get("token")
        project_name = data.get("project_name")
        task_name = data.get("task_name")

        # 检查必要参数是否缺失
        if not all([token, project_name, task_name]):
            return jsonify({"result": False, "message": "Token, project_name, and task_name are required."})

        try:
            # 验证token是否有效并获取用户信息
            user = get_user_by_token(token)  
            if not user:
                return jsonify({"result": False, "message": "Invalid or expired token."})

            # 查找项目是否属于该用户
            project = UserProject.query.filter_by(ProjectName=project_name, user_id=user.UserId).first()
            if not project:
                return jsonify({"result": False, "message": "Project does not exist or does not belong to the user."})

            # 查找任务是否属于该项目
            task = ProjectTask.query.filter_by(TaskName=task_name, user_project_id=project.UserProjectId).first()
            if not task:
                return jsonify({"result": False, "message": "Task does not exist in the specified project."})

            task_path = task.TaskPath  # 保存任务路径，用于删除相关表信息

            # 删除 TaskStatus 表记录
            task_status = TaskStatus.query.filter_by(TaskPath=task_path).first()
            if task_status:
                db.session.delete(task_status)

            # 删除 TaskTime 表记录
            task_time = TaskTime.query.filter_by(TaskPath=task_path).first()
            if task_time:
                db.session.delete(task_time)

            # 删除 ProjectTask 表记录
            db.session.delete(task)
            db.session.commit()

            print(f"{now_time()}: Task '{task_name}' in project '{project_name}' has been successfully deleted.")

            delete_task_request(task_path) # 发送删除请求
            return jsonify({"result": True, "message": None})




        except Exception as e:
            db.session.rollback()
            print(f"{now_time()}: Error occurred while deleting task: {e}")
            logging.error(f"Error occurred while deleting task: {e}")
            return jsonify({"result": False, "message": "An error occurred while deleting the task."})
