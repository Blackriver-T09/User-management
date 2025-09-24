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




class ManualBackup(views.MethodView):
    def post(self):
        try:
            reserve_folder_path = os.path.join(os.path.dirname(__file__), 'reserved')  # 设置备份目录
            backup_database(current_app, reserve_folder_path)  # 使用 current_app 替代直接传递 app
            return jsonify({"result": True, "message": "Database backup completed successfully."})
        except Exception as e:
            logging.error(f"Manual backup failed: {e}")
            return jsonify({"result": False, "message": f"Manual backup failed: {e}"})


