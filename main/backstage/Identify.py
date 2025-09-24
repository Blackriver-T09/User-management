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


from .config import B_USERNAME,B_PASSWORD,SECRETKEY
from .tools import *

iv = os.urandom(16)     # 随机生成一个16字节的 IV, 用于加密时间字符串

class Identify(views.MethodView):
    def get(self):
        return render_template("identify.html")

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        
        # 验证缺失模块
        parameter_list=[username, password]
        for parameter in parameter_list:
            if parameter == None:
                error = "please complete the form!"
                return render_template("identify.html", error=error)


        try:
            if username==B_USERNAME and password == B_PASSWORD:

                key=SECRETKEY
                token = get_encrypted_current_time(key, iv)   #加密后的时间密文作为 token

                return redirect(url_for('dashboard', token=token))

            else:
                error = "wrong information"
                return render_template("identify.html", error=error)



        except Exception as e:
            print(f"{now_time()}: Error during backstage identify: {e}")
            logging.error(f"Error during backstage identify: {e}")
            error ="An unexpected error occurred. Please try again."
            return render_template("identify.html", error=error)
    