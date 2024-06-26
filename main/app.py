from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify
from utils import username_check,password_check,email_check, hash_encipher, decryptor_check,send_email,path_generate,token_generate,tokenTmp_generate


from database.models_user import User
from database.models_token import Token
from database.models_user_project import UserProject
from database.models_project_task import ProjectTask
from database.temp_tokens import TokenTmp
from database.config import Config
from database.config import db

from apscheduler.schedulers.background import BackgroundScheduler  #这个库用于设置定时任务，使tokenTmp 在创建后10分钟自动删除
from datetime import datetime, timedelta, timezone


from flask_cors import CORS,cross_origin

# 增强容错机制
from sqlalchemy.exc import SQLAlchemyError

from services.database_operations import check_user_exists, check_token_exists, check_project_exists, check_task_exists, get_token_by_username, get_username_by_token, get_user_by_token, get_level_by_token, get_password_by_username, get_user_info_by_username, get_projects_by_username, get_tasks_by_project, get_username_by_tokenTmp,get_user_id_by_token


app = Flask(__name__)

app.secret_key = 'my_secret_key'  # 设置一个安全的密钥用于签名会话

app.config.from_object(Config)
CORS(app)

db.app=app
db.init_app(app)





# 定时删除过期tokenTmp
def delete_expired_tokenTmps():
    with app.app_context(): 
        try:
            # 获取10分钟前的UTC时间
            time_threshold = datetime.now(timezone.utc) - timedelta(minutes=10)
            # 查找所有创建时间小于该阈值的tokenTmp
            expired_tokens = TokenTmp.query.filter(TokenTmp.createdAt <= time_threshold).all()
            for token in expired_tokens:
                db.session.delete(token)
            db.session.commit()
            print(f"Deleted {len(expired_tokens)} expired tokenTmp entries.")
        except Exception as e:
            print(f"Failed to delete expired tokenTmps: {e}")
            db.session.rollback()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_tokenTmps, 'interval', minutes=10  )
    scheduler.start()




class Register(views.MethodView):

    
     # 允许所有域进行跨源请求
    def post(self):
        # username = request.form.get('fullname')
        # email = request.form.get('email')
        # institution = request.form.get('institution')
        # password = request.form.get('password')
        # confirm_password = request.form.get('confirm-password')

        data= request.get_json()
        username = data.get('username')
        email = data.get('email')
        institution = data.get('institution')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        username_result, username_error = username_check(username)
        email_result, email_error = email_check(email)
        password_result, password_error = password_check(password)

        # 验证错误模块
        if not username_result:
            return jsonify({'result':False,'error':username_error,'tokenTmp':None})
        if not email_result:
            return jsonify({'result':False,'error':email_error,'tokenTmp':None})
        if not password_result:
            return jsonify({'result':False,'error':password_error,'tokenTmp':None})
        if password != confirm_password:
            return jsonify({'result':False,'error':"confirm password not match your password!",'tokenTmp':None})


        # 所有验证通过，进行注册
        try:
            if check_user_exists(username):
                return jsonify({'result':False,'error':"User already exist",'tokenTmp':None})
            
            # 创建用户信息  
            encrypted_password = hash_encipher(password)
            user = User(Username=username, Password=encrypted_password, Email=email, Organization=institution)
            db.session.add(user)
            db.session.flush()  # Flush to assign ID to user object without committing transaction

            # 创建令牌信息
            token_value = token_generate()
            token = Token(Token=token_value, Level=1, user_id=user.UserId)
            db.session.add(token)
            db.session.commit()

            # 创建临时令牌
            tokenTmp = tokenTmp_generate()  

            # 创建一个 TokenTmp 实例并保存到数据库
            new_token_tmp = TokenTmp(tempToken=tokenTmp, userId=user.UserId)
            db.session.add(new_token_tmp)
            db.session.commit()  

            send_email(email,f'Congratulations,{username}! You have seccessfully register your account for RShub! ',0)

            return jsonify({'result':True,'error':None,'tokenTmp':tokenTmp})
        
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")
            return jsonify({'result':False,'error':"An error occurred during registration. Please try again.",'tokenTmp':None})




class Profile(views.MethodView):

    def post(self):

        data=request.get_json()
        tokenTmp=data.get('tokenTmp')


        # username = session.get('username')  # 从会话获取用户名  
        username=get_username_by_tokenTmp(tokenTmp)


        if username=="token out of date":
            return jsonify({'result':False,'username':None,'token':None,'email':None,'organization':None,'projectlist':None,'error':"token out of date"})

        try:
            basic_info = get_user_info_by_username(username)
            if not basic_info:
                return jsonify({'result':False,'username':None,'token':None,'email':None,'organization':None,'projectlist':None,'error':'Failed to retrieve user information.'})

            email = basic_info.get('Email', "Not Found")
            token = basic_info.get('Token', "No token")
            organization = basic_info.get('Organization', "Not Found")
            projectlist = get_projects_by_username(username)

            if projectlist is None:  # 处理项目列表可能为空的情况
                projectlist = []
                return jsonify({'result':False,'username':None,'token':None,'email':None,'organization':None,'projectlist':None,'error':'Failed to load projects.'})


            return jsonify({'result':True,'username':username,'token':token,'email':email,'organization':organization,'projectlist':projectlist,'error':None})

        except SQLAlchemyError as e:
            return jsonify({'result':False,'username':None,'token':None,'email':None,'organization':None,'projectlist':None,'error':"An internal error occurred. Please try again."})






class Login(views.MethodView):

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        try:
            user_exist = check_user_exists(username)  # 检查用户是否存在
            if user_exist:
                user = User.query.filter_by(Username=username).first()
                password_hashed = get_password_by_username(username)
                if decryptor_check(password, password_hashed):  # 验证密码
                    tokenTmp = tokenTmp_generate()  # 假设 token_generate() 是一个函数来生成一个临时令牌

                    # 创建一个 TokenTmp 实例并保存到数据库
                    new_token_tmp = TokenTmp(tempToken=tokenTmp, userId=user.UserId)
                    db.session.add(new_token_tmp)
                    db.session.commit()  # 提交数据库会话以保存我们的更改

                    return jsonify({'result': True, 'error': None, 'tokenTmp': tokenTmp})
                else:
                    error = "wrong password"
                    return jsonify({'result': False, 'error': error, 'tokenTmp': None})
            else:
                error = "User not exist"
                return jsonify({'result': False, 'error': error, 'tokenTmp': None})

        except SQLAlchemyError as e:
            # flash(f"A database error occurred: {e}", 'error')
            return jsonify({'result': False, 'error': "An internal error occurred. Please try again.", 'tokenTmp': None})
        except Exception as e:
            # flash(f"An unexpected error occurred: {e}", 'error')
            return jsonify({'result': False, 'error': "An unexpected error occurred. Please try again.", 'tokenTmp': None})




class Forget_password(views.MethodView ):
    
    def post(self):
        data = request.get_json()
        email = data.get("email")

        try:
            user_exist = check_user_exists(username)  # 检查用户是否存在
            if user_exist:
                user = User.query.filter_by(Username=username).first()
                password_hashed = get_password_by_username(username)
                if decryptor_check(password, password_hashed):  # 验证密码
                    tokenTmp = tokenTmp_generate()  # 假设 token_generate() 是一个函数来生成一个临时令牌

                    # 创建一个 TokenTmp 实例并保存到数据库
                    new_token_tmp = TokenTmp(tempToken=tokenTmp, userId=user.UserId)
                    db.session.add(new_token_tmp)
                    db.session.commit()  # 提交数据库会话以保存我们的更改

                    return jsonify({'result': True, 'error': None, 'tokenTmp': tokenTmp})
                else:
                    error = "wrong password"
                    return jsonify({'result': False, 'error': error, 'tokenTmp': None})
            else:
                error = "User not exist"
                return jsonify({'result': False, 'error': error, 'tokenTmp': None})

        except SQLAlchemyError as e:
            # flash(f"A database error occurred: {e}", 'error')
            return jsonify({'result': False, 'error': "An internal error occurred. Please try again.", 'tokenTmp': None})
        except Exception as e:
            # flash(f"An unexpected error occurred: {e}", 'error')
            return jsonify({'result': False, 'error': "An unexpected error occurred. Please try again.", 'tokenTmp': None})




    









# 本地API——Project-creation
@app.route('/api/Project-creation', methods=['GET'])
def project_creation():
    token = request.args.get('token')
    project_name = request.args.get('project_name')

    # 检查请求来源是否是本地
    if request.remote_addr != '127.0.0.1':
        abort(403)  # 403错误：权限不足

    try:
        if check_token_exists(token):
            user = get_user_by_token(token)  # 获取与该token相关联的用户对象
            if user:
                project = UserProject(ProjectName=project_name, user_id=user.UserId)
                db.session.add(project)
                db.session.commit()
                return jsonify({'result': True, 'error_message': None})
            else:
                return jsonify({'result': False, "error_message": 'User not found'})
        else:
            return jsonify({'result': False, "error_message": 'Token does not exist'})

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during project creation: {e}")
        return jsonify({'result': False, "error_message": "Database error. Unable to create project."})
    except Exception as e:
        print(f"Unexpected error during project creation: {e}")
        return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again."})





# 本地API——Task-creation
@app.route('/api/Task-creation', methods=['GET'])
def task_creation():
    token = request.args.get('token')
    project_name = request.args.get('project_name')
    task_name = request.args.get('task_name')
    level_required = request.args.get('level', 1)

    # 检查请求来源是否是本地
    if request.remote_addr != '127.0.0.1':
        abort(403)  # 403错误：权限不足

    try:
        if check_token_exists(token):
            user = get_username_by_token(token)
            projects = get_projects_by_username(user)

            if project_name in projects:
                level = get_level_by_token(token)
                
                if level and int(level) >= int(level_required):
                    # 创建新的任务
                    new_task = ProjectTask(TaskName=task_name, TaskPath=path_generate())

                    # 查询项目并将任务与项目关联
                    project = UserProject.query.filter_by(ProjectName=project_name).first()
                    if project:
                        new_task.user_project_id = project.UserProjectId
                        db.session.add(new_task)
                        db.session.commit()

                        return jsonify({'result': True, 'error_message': None, 'path': new_task.TaskPath})
                    else:
                        return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
                else:
                    return jsonify({'result': False, "error_message": 'Insufficient permissions', 'path': None})
            else:
                return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
        else:
            return jsonify({'result': False, "error_message": 'Token does not exist', 'path': None})

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during task creation: {e}")
        return jsonify({'result': False, "error_message": "Database error. Unable to create task.", 'path': None})
    except Exception as e:
        print(f"Unexpected error during task creation: {e}")
        return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again.", 'path': None})




# 本地API—— Download-request
@app.route('/api/Download-request', methods=['GET'])
def download_request():
    token = request.args.get('token')
    project_name = request.args.get('project_name')
    task_name = request.args.get('task_name')

    # 检查请求来源是否是本地
    if request.remote_addr != '127.0.0.1':
        abort(403)  # 403错误：权限不足

    try:
        if check_token_exists(token):
            username = get_username_by_token(token)
            if username:
                projects = get_projects_by_username(username)

                if project_name in projects:
                    user_id=get_user_id_by_token(token)
                    tasks = get_tasks_by_project(user_id,project_name)


                    for task in tasks[::-1]:
                        if task.TaskName == task_name:
                            return jsonify({'result': True, 'error_message': None, 'path': task.TaskPath})
                    return jsonify({'result': False, "error_error_message": 'Task not exist', 'path': None})
                

                    # if task_name in tasks:
                    #     task = ProjectTask.query.filter_by(TaskName=task_name).first()
                    #     if task:
                    #         return jsonify({'result': True, 'error_message': None, 'path': task.TaskPath})
                    #     else:
                    #         return jsonify({'result': False, "error_message": 'Task data retrieval failed', 'path': None})
                    # else:
                    #     return jsonify({'result': False, "error_error_message": 'Task not exist', 'path': None})
                else:
                    return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
            else:
                return jsonify({'result': False, "error_message": 'User not found', 'path': None})
        else:
            return jsonify({'result': False, "error_message": 'Token does not exist', 'path': None})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during download request: {e}")
        return jsonify({'result': False, "error_message": "Database error. Please try again.", 'path': None})
    except Exception as e:
        print(f"Unexpected error during download request: {e}")
        return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again.", 'path': None})






        



# 注册路由
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/', view_func=Login.as_view('main_website'))
app.add_url_rule('/profile', view_func=Profile.as_view('profile'))
app.add_url_rule('/register',view_func=Register.as_view('register'))




# 错误处理模块
@app.errorhandler(404)
def handle_404_error(err):
    # return "发生了错误，错误情况是：%s"%err
    return render_template('404.html')
@app.errorhandler(403)
def handle_404_error(err):
    # return "发生了错误，错误情况是：%s"%err
    return render_template('403.html')




if __name__ == '__main__':
    # with app.app_context():  #创建临时的Flask应用上下文
    #     db.drop_all()  # 删除数据库下的所有 上述定义 的表，防止重复创建
    #     db.create_all()  # 将上述定义的所有表对象映射为数据库下的表单（创建表）

    start_scheduler()    #定时任务启动，每十分钟删除一次过期tokenTmp
    app.run(debug=True)

# session存储了当前用户名




    
