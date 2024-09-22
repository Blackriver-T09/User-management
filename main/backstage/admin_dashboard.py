
from . import admin_api
from flask import jsonify, request
from database import *

@admin_api.route('/dashboard', methods=['GET'])

def dashboard():

    return 'hrllo'


    # # 逻辑处理，如获取数据库信息等
    # user_count = User.query.count()
    # # 其他统计
    # return jsonify({
    #     'user_count': user_count,
    #     'other_info': '...'
    # })
