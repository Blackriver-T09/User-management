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





class Check_credits(views.MethodView):
    def post(self):  
        data=request.get_json()

        token = data.get('token',None)
        credits_needed=data.get('credits',None)

        if token==None:
            return jsonify({'logic':False,'message':'please offer token'})
        
        if credits_needed==None :
            return jsonify({'logic':False,'message':'please offer credits'})



        try:
            responce= get_credits_by_token(token)
            status = responce.get('status',False)
            credits= responce.get('credits',0)
            error_message=responce.get('error message','cant receive responce when checking credits')

        
            if status:
                if credits >= int(credits_needed):    #使用 get 方法获取数据时，返回的类型默认是字符串（str）。无论参数的内容是数字、布尔值还是其他
                    userid=get_user_id_by_token(token)
                    print(f"{now_time()}: User ID {userid} successfully check credits, remains {credits} credits, requires {credits_needed} credits, so access ")
                    return jsonify({'logic':True,'message':None})
                else:
                    userid=get_user_id_by_token(token)
                    print(f"{now_time()}: User ID {userid} successfully check credits, remains {credits} credits, requires {credits_needed} credits, so rejected")
                    return jsonify({'logic':False,'message':'Insufficient remaining credits'})
                
            
            else:
                userid=get_user_id_by_token(token)
                print(f"{now_time()}: User ID {userid} failed to check credits, because of {error_message} ")
                return jsonify({'logic':False,'message':error_message})
            


        except SQLAlchemyError as e:
            print(f"{now_time()}: SQLAlchemyError during Check_credits: {e}")
            logging.error(f"SQLAlchemyError during Check_credits: {e}")
            return jsonify({'logic':False,'message':"An internal error occurred. Please try again."})
        
        except Exception as e:
            print(f"{now_time()}: Error during Check_credits: {e}")
            logging.error(f"Error during Check_credits: {e}")
            return jsonify({'logic':False,'message':"An unexpected error occurred. Please try again."})



