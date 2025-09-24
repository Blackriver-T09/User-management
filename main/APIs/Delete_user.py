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






class DeleteUser(views.MethodView):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        token = data.get("token")  # 增加 token 验证输入

        if not username or not token:
            return jsonify({"result": False, "message": "Please provide both username and token."})

        try:
            # 验证 token 是否有效
            user = get_user_by_token(token)  # 根据 token 获取用户信息
            if not user:
                return jsonify({"result": False, "message": "Invalid token or user not found."})

            # 验证 token 是否与输入的 username 匹配
            if user.Username != username:
                return jsonify({"result": False, "message": "Token does not match the provided username."})

            tokens_deleted = 0
            projects_deleted = 0
            tasks_deleted = 0

            # 删除用户的所有 Token
            tokens = Token.query.filter_by(user_id=user.UserId).all()
            for token in tokens:
                db.session.delete(token)
                tokens_deleted += 1

            # 删除用户的所有 Project 和相关 Task 信息
            projects = UserProject.query.filter_by(user_id=user.UserId).all()
            for project in projects:
                tasks = ProjectTask.query.filter_by(user_project_id=project.UserProjectId).all()
                for task in tasks:
                    task_status = TaskStatus.query.filter_by(TaskPath=task.TaskPath).first()
                    if task_status:
                        db.session.delete(task_status)
                    task_time = TaskTime.query.filter_by(TaskPath=task.TaskPath).first()
                    if task_time:
                        db.session.delete(task_time)
                    db.session.delete(task)                 # 删除任务
                    db.session.flush()                      # 确保删除操作立即应用于数据库
                    delete_task_request(task.TaskPath)      # 异步通知其他服务器删除任务路径（可选）
                    tasks_deleted += 1
                db.session.commit()

                db.session.delete(project)  # 删除 UserProject
                db.session.commit()
                projects_deleted += 1


            db.session.delete(user)  # 删除用户信息
            db.session.commit()  # 提交更改

            print(f"{now_time()}: User '{username}' deleted successfully with {tokens_deleted} tokens, {projects_deleted} projects, and {tasks_deleted} tasks removed.")
            return jsonify({"result": True, "message": f"User '{username}' and all associated data deleted successfully."})

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"{now_time()}: SQLAlchemyError during user deletion: {e}")
            return jsonify({"result": False, "message": "Database error occurred. Please try again later."})

        except Exception as e:
            print(f"{now_time()}: Error during user deletion: {e}")
            return jsonify({"result": False, "message": "An unexpected error occurred. Please try again."})


