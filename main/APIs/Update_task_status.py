import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify,flash
from utils import *


from database import *
import os
import logging
from datetime import datetime, timezone

from flask_cors import CORS,cross_origin

# 增强容错机制
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from services import *




class Update_task_status(views.MethodView):
    def post(self):
        data=request.get_json()
        task_path = data.get('task_path')
        new_job_status=data.get('new_job_status')


        if new_job_status in ['in queue', 'running','completed','failed']:
            pass
        else:
            return jsonify({"result": False, "message": "new_job_status has to be 'in queue','running','completed' or 'failed'"})


        try:
            task_status=get_task_status_by_path(task_path)   #注意返回的是一个对象而不是一个字符串！
            if task_status is None:
                return jsonify({"result": False, "message": "Invalid task path or task path does not exist"})
            

            old_task_status= task_status.Status
            task_status.Status = new_job_status
            task_status.UpdatedAt = datetime.now(timezone.utc)  # 更新时间戳


            # 任务状态更新为 'complete' 时更新结束时间
            if new_job_status == 'completed' and old_task_status != 'completed':
                task_time = TaskTime.query.filter_by(TaskPath=task_path).first()           # 获取与此任务关联的 TaskTime 对象
                if task_time:
                    task_time.EndTime = datetime.now().strftime("%Y-%m-%d %H:%M")  # 设置任务结束时间
                else:
                    # 如果没有找到相应的 TaskTime 记录，可以考虑创建一个新的记录，或记录错误
                    print(f"{now_time()}: No TaskTime entry found for task path '{task_path}'. ")

            db.session.commit()

            print(f"{now_time()}: task with path '{task_path}' has changed from '{old_task_status}' to '{new_job_status}' ")
            return jsonify({"result": True, "message": None})

            
        except SQLAlchemyError as e:
            db.session.rollback()  # 回滚在出现异常时的所有更改
            print(f"{now_time()}: SQLAlchemyError during Update_task_status: {e}")
            logging.error(f"SQLAlchemyError during Update_task_status: {e}")
            return jsonify({"result": False, "message": "Database error."})
        
        except Exception as e:
            print(f"{now_time()}: Error during Update_task_status: {e}")
            logging.error(f"Error during Update_task_status: {e}")
            return jsonify({"result": False, "message": "An unexpected error occurred."})




