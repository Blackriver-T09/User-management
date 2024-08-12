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




class Update_task_status(views.MethodView):
    def post():
        data=request.get_json()
        task_path = data.get('task_path')
        new_job_status=data.get('credits')


        try:
            pass

        except SQLAlchemyError as e:
            db.session.rollback()  # 回滚在出现异常时的所有更改
            print(f"{now_time()}: SQLAlchemyError during Update_task_status: {e}")
            logging.error(f"SQLAlchemyError during Update_task_status: {e}")
            return jsonify({"result": False, "message": "Database error."})
        
        except Exception as e:
            print(f"{now_time()}: Error during Update_task_status: {e}")
            logging.error(f"Error during Update_task_status: {e}")
            return jsonify({"result": False, "message": "An unexpected error occurred."})




