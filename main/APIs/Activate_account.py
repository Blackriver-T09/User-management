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







# 这个页面只能从邮件中打开
class Activate(views.MethodView):
    def get(self, tokenTmp):


        # 如果链接已经过期
        username = get_username_by_tokenTmp(tokenTmp)
        if username in ["token out of date", "user not exist"]:
            result='This link is expired!'
            prompt='Please register again'
            return render_template('activate_account_succesfully.html',result=result,prompt=prompt)

        # 如果找不到用户
        user = User.query.filter_by(Username=username).first()
        if not user:
            result="You haven't registered yet!"
            prompt='Please register again'
            return render_template('activate_account_succesfully.html',result=result,prompt=prompt)

        # 检查账户是否已激活
        if user.Activated:
            result = "Your account is already active."
            prompt = "No further actions are required."
            return render_template('activate_account_successfully.html', result=result, prompt=prompt)

        try:
            # 创建令牌信息
            token_value = token_generate()
            token = Token(Token=token_value, Level=1, user_id=user.UserId)
            db.session.add(token)
            db.session.flush()

            # 激活账号
            user.Activated=True
            db.session.commit()


            print(f'{now_time()}: {username} has registered Successfully')


            result='Your account has been activated!'
            prompt='Now you can easily log in!'
            return render_template('activate_account_succesfully.html',result=result,prompt=prompt)
        


        except Exception as e:
            db.session.rollback()
            result = "Activation failed due to a server error."
            prompt = "Please try again later."
            print(f"{now_time()}: Error during account activation for {username}: {str(e)}")
            logging.error(f"Error during account activation for {username}: {str(e)}")
            return render_template('activate_account_successfully.html', result=result, prompt=prompt)


