from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify,flash
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
import subprocess
import os
import logging
import time


from flask_cors import CORS,cross_origin

# 增强容错机制
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from services.database_operations import check_user_exists, check_token_exists, check_project_exists, check_task_exists, get_token_by_username, get_username_by_token, get_user_by_token, get_level_by_token, get_password_by_username, get_user_info_by_username, get_projects_by_username, get_tasks_by_project, get_username_by_tokenTmp,get_user_id_by_token,verify_user_email


app = Flask(__name__)
app.secret_key = 'my_secret_key'  # 设置一个安全的密钥用于签名会话

app.config.from_object(Config)
CORS(app)

db.app=app
db.init_app(app)






# 配置日志
logging.basicConfig(filename='./log/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
file_handler = logging.FileHandler('./log/app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 配置日志处理器
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# 调整SQLAlchemy的日志级别
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.setLevel(logging.WARNING)










def now_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")



# 删除过期的tokenTmp
def delete_expired_tokenTmps():
    with app.app_context():
        try:
            # 获取10分钟前的UTC时间
            time_threshold = datetime.now(timezone.utc) - timedelta(minutes=10)
            # 查找所有创建时间小于该阈值的tokenTmp
            expired_tokens = TokenTmp.query.filter(TokenTmp.createdAt <= time_threshold).all()
            count = len(expired_tokens)
            for token in expired_tokens:
                db.session.delete(token)
            db.session.commit()

            print(f'{now_time()}: Deleted {count} expired tokenTmp entries.')
            logging.info(f"Deleted {count} expired tokenTmp entries.")
        except Exception as e:
            db.session.rollback()

            print(f"{now_time()}: Failed to delete expired tokenTmps: {e}")
            logging.error(f"Failed to delete expired tokenTmps: {e}")

# 数据库备份任务
def backup_database():
    try:
        # 读取数据库配置
        db_user = app.config['MYSQL_USER']
        db_password = app.config['MYSQL_PASSWORD']
        db_name = app.config['MYSQL_DB']


        # 确保备份目录存在
        backup_dir = os.path.join(os.path.dirname(__file__), 'reserved')
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, f"{db_name}_backup.sql")   #每次运行备份脚本时新的备份文件会覆盖前一次的备份文件
        # 如果要保留历史备份文件，可以在文件名中包含当前日期和时间的时间戳
        # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # backup_path = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")

        command = f"mysqldump -u {db_user} -p{db_password} {db_name} > {backup_path}"
        result = subprocess.run(command, shell=True, check=True)

        if result.returncode == 0:

            print(f'{now_time()}: Database backup completed successfully.')
            logging.info("Database backup completed successfully.")
        else:
            print(f'{now_time()}: Database backup failed.')
            logging.error("Database backup failed.")

    except subprocess.CalledProcessError as e:
        print(f'{now_time()}: Backup command failed with exit status {e.returncode}')
        logging.error(f"Backup command failed with exit status {e.returncode}")

    except Exception as e:
        print(f'{now_time()}: Error executing backup: {e}')
        logging.error(f"Error executing backup: {e}")

# 检查数据库备份文件的大小
def check_db_size():
    try:
        backup_dir = os.path.join(os.path.dirname(__file__), 'reserved')
        backup_path = os.path.join(backup_dir, f"{app.config['MYSQL_DB']}_backup.sql")
        file_size = os.path.getsize(backup_path)

        print(f'{now_time()}: Database file size: {file_size} bytes')
        logging.info(f"Database file size: {file_size} bytes")
    except FileNotFoundError:

        print(f'{now_time()}: Backup file does not exist.')
        logging.error("Backup file does not exist.")
    except Exception as e:

        print(f'{now_time()}: Failed to check database file size: {e}')
        logging.error(f"Failed to check database file size: {e}")



def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_tokenTmps, 'interval', minutes=10)  # 保留这个任务每10分钟运行一次，以清理过期的 tokenTmp

    # 将数据库备份和文件大小检查任务设置为每24小时执行一次
    # 设置了next_run_time来控制首次任务执行的具体时间。
    # 备份数据库任务将在启动调度器10秒后开始执行，而检查数据库文件大小的任务则会在40秒后开始执行。
    scheduler.add_job(backup_database, 'interval', hours=24, next_run_time=datetime.now() + timedelta(seconds=10))  # 10秒后开始第一次备份
    scheduler.add_job(check_db_size, 'interval', hours=24, next_run_time=datetime.now() + timedelta(seconds=40))  # 40秒后开始第一次文件大小检查

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

            print(f'{now_time()}: {username} has registered Successfully')

            return jsonify({'result':True,'error':None,'tokenTmp':tokenTmp})
        
        except Exception as e:
            db.session.rollback()

            print(f"{now_time()}: Error during registration: {e}")
            logging.error(f"Error during registration: {e}")

            return jsonify({'result':False,'error':"An error occurred during registration. Please try again.",'tokenTmp':None})




class Profile(views.MethodView):

    def post(self):

        data=request.get_json()
        tokenTmp=data.get('tokenTmp')


        # username = session.get('username')  # 从会话获取用户名  
        username=get_username_by_tokenTmp(tokenTmp)


        if username=="token out of date":
            return jsonify({'result':False,'username':None,'token':None,'email':None,'organization':None,'projectlist':None,'error':"token out of date"})
        elif username =="user not exist":
            return jsonify({'result':False,'username':None,'token':None,'email':None,'organization':None,'projectlist':None,'error':"user not exist"})


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


            print(f"{now_time()}: {username} has successfully visited his/her page")
            return jsonify({'result':True,'username':username,'token':token,'email':email,'organization':organization,'projectlist':projectlist,'error':None})

        except SQLAlchemyError as e:

            print(f"{now_time()}: SQLAlchemyError during Profile: {e}")
            logging.error(f"SQLAlchemyError during Profile: {e}")

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

                    print(f"{now_time()}: {username} has successfully log in")
                    return jsonify({'result': True, 'error': None, 'tokenTmp': tokenTmp})
                else:
                    error = "wrong password"
                    return jsonify({'result': False, 'error': error, 'tokenTmp': None})
            else:
                error = "User not exist"
                return jsonify({'result': False, 'error': error, 'tokenTmp': None})

        except SQLAlchemyError as e:
            # flash(f"A database error occurred: {e}", 'error')
            print(f"{now_time()}: SQLAlchemyError during Login: {e}")
            logging.error(f"SQLAlchemyError during Login: {e}")

            return jsonify({'result': False, 'error': "An internal error occurred. Please try again.", 'tokenTmp': None})
        except Exception as e:
            # flash(f"An unexpected error occurred: {e}", 'error')

            print(f"{now_time()}: Error during Login: {e}")
            logging.error(f"Error during Login: {e}")
            return jsonify({'result': False, 'error': "An unexpected error occurred. Please try again.", 'tokenTmp': None})





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





    


# Web API——发送邮件
@app.route('/api/email',methods=['POST'])
def email_request():
    data=request.get_json()
    email=data.get('email')
    username = data.get("username")

    try:
        user_exist = check_user_exists(username)  # 检查用户是否存在
        if user_exist:
            user = User.query.filter_by(Username=username).first()

            if verify_user_email(username, email):

                # 创建一个 TokenTmp 实例并保存到数据库
                tokenTmp = tokenTmp_generate()  # 假设 token_generate() 是一个函数来生成一个临时令牌
                new_token_tmp = TokenTmp(tempToken=tokenTmp, userId=user.UserId)
                db.session.add(new_token_tmp)
                db.session.commit()  # 提交数据库会话以保存我们的更改
                
                # 构建重置密码的 URL
                reset_url = url_for('change_password', tokenTmp=tokenTmp, _external=True)
                # reset_url = 'https://rshub.zju.edu.cn/change-password/' + tokenTmp


                # 准备邮件内容
                message = f'Hello {username},\n\nWe received your request to reset your password. Please click the link below to reset your password. This link will expire in 10 minutes:\n{reset_url}\n\nIf you did not request this change, please ignore this email.'


                try:
                    send_email(email,message,1) 


                    print(f"{now_time()}: change_password email has been sent to {username} ")
                    return jsonify({'result': True, 'error': None})
                except Exception as e:

                    print(f"{now_time()}: error happened whenn sending email:{e}")
                    logging.error(f"error happened whenn sending email:{e}")
                    return jsonify({'result': False, 'error': f"error happened whenn sending email:{e}"})
            
            else:
                error="email doesn't match this username"
                return jsonify({'result': False, 'error': error})
        else:
            error = "User not exist"
            return jsonify({'result': False, 'error': error})

    except SQLAlchemyError as e:
        # flash(f"A database error occurred: {e}", 'error')

        print(f"{now_time()}: SQLAlchemyError during Email: {e}")
        logging.error(f"SQLAlchemyError during Email: {e}")
        return jsonify({'result': False, 'error': "An internal error occurred. Please try again."})
    except Exception as e:
        # flash(f"An unexpected error occurred: {e}", 'error')

        print(f"{now_time()}: Error during Email: {e}")
        logging.error(f"Error during Email: {e}")
        return jsonify({'result': False, 'error': "An unexpected error occurred. Please try again."})








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

                print(f"{now_time()}: {user.Username} successfully create project {project_name}")
                return jsonify({'result': True, 'error_message': None})
            else:
                return jsonify({'result': False, "error_message": 'User not found'})
        else:
            return jsonify({'result': False, "error_message": 'Token does not exist'})

    except SQLAlchemyError as e:
        db.session.rollback()

        print(f"{now_time()}: SQLAlchemyError during project_creation: {e}")
        logging.error(f"SQLAlchemyError during project_creation: {e}")
        return jsonify({'result': False, "error_message": "Database error. Unable to create project."})
    except Exception as e:
        
        print(f"{now_time()}: Error during project_creation: {e}")
        logging.error(f"Error during project_creation: {e}")
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

                        print(f"{now_time()}: {user.Username} successfully create task '{task_name}' in project '{project_name}'")
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

        print(f"{now_time()}: SQLAlchemyError during Task-creation: {e}")
        logging.error(f"SQLAlchemyError during Task-creation: {e}")
        return jsonify({'result': False, "error_message": "Database error. Unable to create task.", 'path': None})
    except Exception as e:

        print(f"{now_time()}: Error during Task-creation: {e}")
        logging.error(f"Error during Task-creation: {e}")
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


                            print(f"{now_time()}: {username} successfully Download request")
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

        print(f"{now_time()}: SQLAlchemyError during download_request: {e}")
        logging.error(f"SQLAlchemyError during download_request: {e}")
        return jsonify({'result': False, "error_message": "Database error. Please try again.", 'path': None})
    except Exception as e:
        
        print(f"{now_time()}: Error during download_request: {e}")
        logging.error(f"Error during download_request: {e}")
        return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again.", 'path': None})






        



# 注册路由
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/', view_func=Login.as_view('main_website'))
app.add_url_rule('/profile', view_func=Profile.as_view('profile'))
app.add_url_rule('/register',view_func=Register.as_view('register'))
app.add_url_rule('/change-password/<tokenTmp>', view_func=Change_password.as_view('change_password'), methods=['GET', 'POST'])

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

    start_scheduler()    #定时任务启动，每十分钟删除一次过期tokenTmp
    app.run(debug=True)






