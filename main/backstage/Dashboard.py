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

from .config import B_USERNAME,B_PASSWORD,SECRETKEY,MINS
from .tools import *



class Dashboard(views.MethodView):
    def get(self, token):
        mins = MINS
        key = SECRETKEY
        if is_token_valid(token, key, mins):     # 验证解密后的时间和当前时间差异是否在3分钟内
            return render_template('dashboard.html',token=token)
        else:
            return 'Token out of date'

    def post(self):
        pass


