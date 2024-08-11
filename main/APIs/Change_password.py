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

from services.database_operations import check_user_exists, check_token_exists, check_project_exists, check_task_exists, get_token_by_username, get_username_by_token, get_user_by_token, get_level_by_token, get_password_by_username, get_user_info_by_username, get_projects_by_username, get_tasks_by_project, get_username_by_tokenTmp,get_user_id_by_token,verify_user_email
from services.scheduler_tasks  import now_time,start_scheduler






# 这个页面只能从邮件中打开
class Change_password(views.MethodView):
    def get(self, tokenTmp):
        return render_template('change_password.html', tokenTmp=tokenTmp)

    def post(self, tokenTmp):
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-new-password')

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('change_password', tokenTmp=tokenTmp))
        
        # 验证密码强度
        password_result, password_error = password_check(new_password)
        if not password_result:
            flash(password_error, 'error')
            return redirect(url_for('change_password', tokenTmp=tokenTmp))


        try:
            username = get_username_by_tokenTmp(tokenTmp)
            if username in ["token out of date", "user not exist"]:
                flash(username, 'error')
                return redirect(url_for('change_password', tokenTmp=tokenTmp))

            user = User.query.filter_by(Username=username).first()
            if not user:
                flash('Cannot find this user.', 'error')
                return redirect(url_for('change_password', tokenTmp=tokenTmp))

            # 更新用户密码
            user.Password = hash_encipher(new_password)
            db.session.commit()

            print(f"{now_time()}: {username} has change password successfully.")
            return render_template('change_password_succesfully.html')

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"A database error occurred: {e}", 'error')


            print(f"{now_time()}: SQLAlchemyError during Change_password: {e}")
            logging.error(f"SQLAlchemyError during Change_password: {e}")
            return redirect(url_for('change_password', tokenTmp=tokenTmp))
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'error')

            print(f"{now_time()}: Error during Change_password: {e}")
            logging.error(f"Error during Change_password: {e}")
            return redirect(url_for('change_password', tokenTmp=tokenTmp))

