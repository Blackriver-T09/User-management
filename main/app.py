from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify,flash
from utils import username_check,password_check,email_check, hash_encipher, decryptor_check,alert,path_generate,token_generate

from database.models_user import User
from database.models_token import Token
from database.models_user_project import UserProject
from database.models_project_task import ProjectTask
from database.config import Config
from database.config import db

from flask_cors import CORS,cross_origin

# 增强容错机制
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)


app.secret_key = 'my_secret_key'  # 设置一个安全的密钥用于签名会话

app.config.from_object(Config)
CORS(app)

db.app=app
db.init_app(app)



def check_user_exists(username):
    try:
        user = User.query.filter_by(Username=username).first()
        return bool(user)  # 用户存在返回True，不存在返回False
    except SQLAlchemyError as e:
        # 处理可能的数据库查询错误
        print(f"Database error occurred: {e}")
        return None  # 数据库错误时返回None

def check_token_exists(token_value):
    try:
        token = Token.query.filter_by(Token=token_value).first()
        return bool(token)  # 令牌存在返回True，不存在返回False
    except SQLAlchemyError as e:
        # 处理可能的数据库查询错误
        print(f"Database error occurred: {e}")
        return None  # 数据库错误时返回None

def check_project_exists(project_name):
    try:
        project = UserProject.query.filter_by(ProjectName=project_name).first()
        return bool(project)  # 如果存在该项目，返回True，否则返回False
    except SQLAlchemyError as e:
        # 记录数据库查询错误
        print(f"Database error occurred when checking project existence: {e}")
        return None  # 数据库错误时返回None，表示无法确定项目是否存在


def check_task_exists(task_name):
    try:
        task = ProjectTask.query.filter_by(TaskName=task_name).first()
        return bool(task)  # 如果存在该任务，返回True，否则返回False
    except SQLAlchemyError as e:
        # 记录数据库查询错误
        print(f"Database error occurred when checking task existence: {e}")
        return None  # 数据库错误时返回None，表示无法确定任务是否存在


def get_token_by_username(username):
    try:
        user = User.query.filter_by(Username=username).first()
        if user:
            token = Token.query.filter_by(user_id=user.UserId).first()
            if token:
                return token.Token
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving token by username: {e}")
    return None  # 如果发生错误或找不到令牌，返回None



def get_username_by_token(token):
    try:
        user = User.query.join(Token, User.UserId == Token.user_id).filter(Token.Token == token).first()
        if user:
            return user.Username
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving username by token: {e}")
    return None  # 如果发生错误或找不到用户，返回None

    


def get_user_by_token(token):
    try:
        # 使用 join 来连接 User 和 Token 表，并查找匹配的用户
        user = User.query.join(Token, User.UserId == Token.user_id).filter(Token.Token == token).first()
        return user  # 返回 User 对象或 None
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving user by token: {e}")
        return None  # 发生数据库错误时返回 None



def get_level_by_token(token_value):
    try:
        token = Token.query.filter_by(Token=token_value).first()
        if token:
            return token.Level  # 返回令牌的级别
        return None  # 未找到令牌时返回 None
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving level by token: {e}")
        return None  # 发生数据库错误时返回 None



def get_password_by_username(username):
    try:
        user = User.query.filter_by(Username=username).first()
        if user:
            return user.Password  # 返回用户密码
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving password by username: {e}")
    return None  # 如果发生错误或用户名不存在，返回 None

    

def get_user_info_by_username(username):
    try:
        user = User.query.filter_by(Username=username).first()
        if user:
            token = Token.query.filter_by(user_id=user.UserId).first()
            return {
                "Email": user.Email,
                "Token": token.Token if token else 'No token',
                "Organization": user.Organization
            }
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving user info by username: {e}")
    return None  # 如果发生错误或找不到用户，返回 None



def get_projects_by_username(username):
    try:
        user = User.query.filter_by(Username=username).first()
        if user:
            projects = UserProject.query.filter_by(user_id=user.UserId).all()
            return [project.ProjectName for project in projects]  # 返回项目名列表
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving projects by username: {e}")
    return None  # 如果发生错误或找不到项目，返回 None


def get_tasks_by_project(project_name):
    try:
        project = UserProject.query.filter_by(ProjectName=project_name).first()
        if project:
            tasks = ProjectTask.query.filter_by(user_project_id=project.UserProjectId).all()
            return [task.TaskName for task in tasks]  # 返回任务名列表
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving tasks by project: {e}")
    return None  # 如果发生错误或找






class Register(views.MethodView):
    # def get(self):
    #     return render_template('register.html')
    
     # 允许所有域进行跨源请求
    def post(self):
        # username = request.form.get('fullname')
        # email = request.form.get('email')
        # institution = request.form.get('institution')
        # password = request.form.get('password')
        # confirm_password = request.form.get('confirm-password')
        data= request.get_json()
        username = data.get('fullname')
        email = data.get('email')
        institution = data.get('institution')
        password = data.get('password')
        confirm_password = data.get('confirm-password')

        username_result, username_error = username_check(username)
        email_result, email_error = email_check(email)
        password_result, password_error = password_check(password)

        # 验证错误模块
        if not username_result:
            # return render_template('register.html', error=username_error)
            return jsonify({'result':False,'error':username_error,'token':None})
        if not email_result:
            # return render_template('register.html', error=email_error)
            return jsonify({'result':False,'error':email_error,'token':None})
        if not password_result:
            # return render_template('register.html', error=password_error)
            return jsonify({'result':False,'error':password_error,'token':None})
        if password != confirm_password:
            # return render_template('register.html', error="confirm password not match your password!")
            return jsonify({'result':False,'error_message':"confirm password not match your password!",'token':None})


        # 所有验证通过，进行注册
        try:
            if check_user_exists(username):
                # return render_template('register.html', error="用户名已存在")
                return jsonify({'result':False,'error_message':"User already exist",'token':None})
            
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

            session['username'] = username
            # return redirect(url_for('user'))  
            return jsonify({'result':True,'error_message':None,'token':None})
        
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")
            # return render_template('register.html', error="An error occurred during registration. Please try again.")
            return jsonify({'result':False,'error_message':"An error occurred during registration. Please try again.",'token':None})




class Profile(views.MethodView):
    

    def get(self):
        username = session.get('username')  # 从会话获取用户名  
        if not username:
            flash('You are not logged in.', 'warning')
            return redirect(url_for('login'))  # 如果没有用户名，则重定向到登录页面

        try:
            basic_info = get_user_info_by_username(username)
            if not basic_info:
                flash('Failed to retrieve user information.', 'error')
                return redirect(url_for('login'))  # 如果未找到用户信息，则可能需要重新登录

            email = basic_info.get('Email', "Not Found")
            token = basic_info.get('Token', "No token")
            organization = basic_info.get('Organization', "Not Found")
            projectlist = get_projects_by_username(username)

            if projectlist is None:  # 处理项目列表可能为空的情况
                projectlist = []
                flash('Failed to load projects.', 'error')

            return render_template('profile.html', username=username, key=token, email=email, organization=organization, projects=projectlist)

        except SQLAlchemyError as e:
            flash(f'An error occurred: {e}', 'error')
            # return redirect(url_for('login'))  # 在发生数据库错误时重定向到登录页面
            return jsonify({'result':False,'error_message':"An internal error occurred. Please try again."})






class Login(views.MethodView):
    # def get(self):
    #     return render_template("login.html")

    def post(self):
        data= request.get_json()
        username =data.get("username")
        password =data.get("password")

        try:
            user_exist = check_user_exists(username)  # 检查用户是否存在
            if user_exist:
                password_hashed = get_password_by_username(username)
                if decryptor_check(password, password_hashed):  # 验证密码
                    session['username'] = username
                    # return redirect(url_for('user'))  # 登录成功，重定向到用户页面
                    return jsonify({'result':True,'error_message':None,'token':None})
                else:
                    error = "wrong password"
                    # return render_template("login.html", error=error)
                    return jsonify({'result':False,'error_message':error,'token':None})
            else:
                error = "User not exist"
                # return render_template("login.html", error=error)
                return jsonify({'result':False,'error_message':error,'token':None})

        except SQLAlchemyError as e:
            flash(f"A database error occurred: {e}", 'error')
            # return render_template("login.html", error="An internal error occurred. Please try again.")
            return jsonify({'result':False,'error_message':"An internal error occurred. Please try again.",'token':None})
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", 'error')
            # return render_template("login.html", error="An unexpected error occurred. Please try again.")
            return jsonify({'result':False,'error_message':"An unexpected error occurred. Please try again.",'token':None})




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
                return jsonify({'result': True, 'error_message': None,'token':None})
            else:
                return jsonify({'result': False, "error_message": 'User not found','token':None})
        else:
            return jsonify({'result': False, "error_message": 'Token does not exist','token':None})

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during project creation: {e}")
        return jsonify({'result': False, "error_message": "Database error. Unable to create project.",'token':None})
    except Exception as e:
        print(f"Unexpected error during project creation: {e}")
        return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again.",'token':None})





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
        return jsonify({'result': False, "error_message": "Database error. Unable to create task."})
    except Exception as e:
        print(f"Unexpected error during task creation: {e}")
        return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again."})




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
            user = get_username_by_token(token)
            if user:
                projects = get_projects_by_username(user)

                if project_name in projects:
                    tasks = get_tasks_by_project(project_name)

                    if task_name in tasks:
                        task = ProjectTask.query.filter_by(TaskName=task_name).first()
                        if task:
                            return jsonify({'result': True, 'error_message': None, 'path': task.TaskPath})
                        else:
                            return jsonify({'result': False, "error_message": 'Task data retrieval failed', 'path': None})
                    else:
                        return jsonify({'result': False, "error_error_message": 'Task not exist', 'path': None})
                else:
                    return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
            else:
                return jsonify({'result': False, "error_message": 'User not found', 'path': None})
        else:
            return jsonify({'result': False, "error_message": 'Token does not exist', 'path': None})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during download request: {e}")
        return jsonify({'result': False, "error_message": "Database error. Please try again."})
    except Exception as e:
        print(f"Unexpected error during download request: {e}")
        return jsonify({'result': False, "error_message": "An unexpected error occurred. Please try again."})






        



# 注册路由
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/', view_func=Login.as_view('main_website'))
app.add_url_rule('/user', view_func=Profile.as_view('user'))
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
    app.run(debug=True)

# session存储了当前用户名
