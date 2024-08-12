
from . import admin_api
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from database import *

@admin_api.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    # 逻辑处理，如获取数据库信息等
    user_count = User.query.count()
    # 其他统计
    return jsonify({
        'user_count': user_count,
        'other_info': '...'
    })
