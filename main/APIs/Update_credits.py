import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify,flash
from utils import username_check,password_check,email_check, hash_encipher, decryptor_check,send_email,path_generate,token_generate,tokenTmp_generate


from database.models_user import User
from database.models_token import Token
from database.models_user_project import UserProject
from database.models_project_task import ProjectTask
from database.temp_tokens import TokenTmp
from database.config import Config
from database.config import db
import os
import logging
import time

from flask_cors import CORS,cross_origin

# 增强容错机制
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from services.database_operations import *
from services.scheduler_tasks  import *





class Update_credits(views.MethodView):
    def post(self):  
        data=request.get_json()

        token = data.get('token')
        credits_needed=data.get('credits')


            
        try:
            user = get_user_by_token(token)
            if not user:
                return jsonify({"result": False, "message": "Invalid token or user does not exist."})


            if user.Credits < credits_needed:          # 检查用户是否有足够的 credits
                return jsonify({"result": False, "message": "Insufficient credits."})


            user.Credits -= credits_needed
            newcredits = user.Credits
            db.session.commit()  # 提交更改到数据库

            userid=get_user_id_by_token(token)
            print(f"{now_time()}: User ID {userid} has successfully updated credits to {newcredits}( change size:{-credits_needed}) ")
            return jsonify({"result": True, "message": None})

        except SQLAlchemyError as e:
            db.session.rollback()  # 回滚在出现异常时的所有更改
            print(f"{now_time()}: SQLAlchemyError during Update_credits: {e}")
            logging.error(f"SQLAlchemyError during Update_credits: {e}")
            return jsonify({"result": False, "message": "Database error."})
        
        except Exception as e:
            print(f"{now_time()}: Error during Update_credits: {e}")
            logging.error(f"Error during Update_credits: {e}")
            return jsonify({"result": False, "message": "An unexpected error occurred."})







