from flask import Flask, render_template, request, views, url_for, redirect, session,abort,jsonify
from utils import username_check,password_check,email_check, hash_encipher, decryptor_check,alert,path_generate,token_generate

from database.models_user import User
from database.models_token import Token
from database.models_user_project import UserProject
from database.models_project_task import ProjectTask
from database.config import Config
from database.config import db




app = Flask(__name__)
app.secret_key = 'my_secret_key'  # 设置一个安全的密钥用于签名会话

app.config.from_object(Config)

db.app=app
db.init_app(app)



def check_user_exists(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        return True  # 用户存在
    return False  # 用户不存在

def check_token_exists(token_value):
    token = Token.query.filter_by(Token=token_value).first()
    if token:
        return True  # 令牌存在
    return False  # 令牌不存在

def check_project_exists(project_name):
    # 根据给定的项目名查询数据库中是否存在该项目
    project = UserProject.query.filter_by(ProjectName=project_name).first()
    if project:
        return True  # 如果存在该项目，返回True
    else:
        return False  # 如果不存在该项目，返回False
    
def check_task_exists(task_name):
    # 根据给定的任务名查询数据库中是否存在该任务
    task = ProjectTask.query.filter_by(TaskName=task_name).first()
    if task:
        return True  # 如果存在该任务，返回True
    else:
        return False  # 如果不存在该任务，返回False


def get_token_by_username(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        token = Token.query.filter_by(user_id=user.UserId).first()
        if token:
            return token.Token
    return None

def get_username_by_token(token):
    # 根据给定的token查询与之关联的用户信息
    user = User.query.join(Token).filter(Token.Token == token).first()
    if user:
        return user.Username
    else:
        return None  # 如果找不到用户，返回None或者其他你认为合适的值
    

def get_user_by_token(token):
    # 根据给定的token查询与之关联的用户对象
    user = User.query.join(Token).filter(Token.Token == token).first()
    return user  # 返回 User 对象或 None



def get_level_by_token(token_value):
    token = Token.query.filter_by(Token=token_value).first()
    if token:
        return token.Level
    return None

def get_password_by_username(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        return user.Password
    else:
        return None  # 如果用户名不存在，返回 None 或者其他你认为合适的值
    
def get_user_info_by_username(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        token = Token.query.filter_by(user_id=user.UserId).first()
        return {
            "Email": user.Email,
            "Token": token.Token if token else 'No token',
            "Organization": user.Organization
        }
    return None

def get_projects_by_username(username):
    user = User.query.filter_by(Username=username).first()
    if user:
        projects = UserProject.query.filter_by(user_id=user.UserId).all()
        return [project.ProjectName for project in projects]
    return None

def get_tasks_by_project(project_name):
    project = UserProject.query.filter_by(ProjectName=project_name).first()
    if project:
        tasks = ProjectTask.query.filter_by(user_project_id=project.UserProjectId).all()
        return [task.TaskName for task in tasks]
    return None







class Register(views.MethodView):
    def get(self):
            return render_template('register.html')
    def post(self):

        username=request.form.get('fullname')
        email=request.form.get('email') 
        institution=request.form.get('institution')
        password=request.form.get('password')
        confirm_password=request.form.get('confirm-password')


        username_result,username_error=username_check(username)
        email_result,email_error=email_check(email)
        password_result,password_error=password_check(password)

        if username_result:
            if email_result:
                if password_result:
                    if password==confirm_password:  
                        if check_user_exists(username):
                            return render_template('register.html',error="用户名已存在")
                        else:  #所有验证都已经通过
                            session['username'] = username



                            # 创建用户信息
                            user = User(Username=username, Password=hash_encipher(password), Email=email, Organization=institution)
                            db.session.add(user)
                            db.session.commit()

                            # 创建令牌信息
                            token = Token(Token=token_generate(), Level=1, user_id=user.UserId)
                            db.session.add(token)
                            db.session.commit()

                            
                            # user_list[username] = hash_encipher(password)
                            # # token_list[username] = token_generate()
                            # email_list[username] = email
                        return redirect(url_for('user')) 
                    else:
                        return render_template('register.html',error="确认密码不匹配！")
                else:
                    return render_template('register.html',error=password_error)
            else:
                return render_template('register.html',error=email_error)
        else:
            return render_template('register.html',error=username_error)



class Profile(views.MethodView):
    def get(self):
        username = session.get('username')  # 从会话获取用户名
        if not username:
            return redirect(url_for('login'))  # 如果没有用户名，则重定向到登录页面
        
        # token = get_token_by_username(username)  
        basic_info=get_user_info_by_username(username)
        email=basic_info.get('Email',"Not Found")
        token=basic_info.get('Token',"Not Found")
        organization=basic_info.get('Organization',"Not Found")

        projectlist=get_projects_by_username(username)

        return render_template('profile.html', username=username, key=token,email=email, organization=organization, projects=projectlist)



class Login(views.MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        user_exist=check_user_exists(username)  # 用户是否存在


        if user_exist :
            password_hashed=get_password_by_username(username)

            if decryptor_check(password,password_hashed):
                session['username'] = username
                return redirect(url_for('user'))  #随后User类去session中查询用户名
            else:
                error =  "密码错误"  
                return render_template("login.html", error=error)  #出现错误时，把错误信息传到login.html里，这样就不会重定向到一个新的网页
        
        else:
            error =  "用户不存在"  #error存储错误信息，要么是 “密码错误” 要么是 “用户不存在”
            return render_template("login.html", error=error)  #出现错误时，把错误信息传到login.html里，这样就不会重定向到一个新的网页











# 本地API——Project-creation 
@app.route('/api/Project-creation', methods=['GET'])
def project_creation():
    token = request.args.get('token')
    Project_name = request.args.get('project_name')

    if request.remote_addr != '127.0.0.1':
        abort(403)  # 权限不足

    if check_token_exists(token):
        user = get_user_by_token(token)  # 获取与该token相关联的用户对象
        if user:
            project = UserProject(ProjectName=Project_name, user_id=user.UserId)
            db.session.add(project)
            db.session.commit()
            return jsonify({'result': True, 'error_message': None})
        else:
            return jsonify({'result': False, "error_message": 'User not found'})
    else:
        return jsonify({'result': False, "error_message": 'token not exist'})





# 本地API—— Task-creation 
@app.route('/api/Task-creation', methods=['GET'])
def task_creation():

    token=request.args.get('token')
    Project_name=request.args.get('project_name')
    task_name=request.args.get('task_name')
    level_required=request.args.get('level',1)


    # 检查请求来源是否是本地
    if request.remote_addr != '127.0.0.1':
        abort(403)  # 403错误：权限不足

    if check_token_exists(token):

        user = get_username_by_token(token)
        projects=get_projects_by_username(user)

        if Project_name in projects:
            level= get_level_by_token(token)
            
            if int(level)>=int(level_required):
                # 1. 创建新的任务
                new_task = ProjectTask(TaskName=task_name, TaskPath=path_generate())

                # 2. 查询项目并将任务与项目关联
                project = UserProject.query.filter_by(ProjectName=Project_name).first()
                if project:
                    new_task.user_project_id = project.UserProjectId
                    db.session.add(new_task)
                    db.session.commit()

                    return jsonify({'result': True, 'error_message': None, 'path': new_task.TaskPath})
                else:
                    return jsonify({'result': False, "error_message": 'Project not exist', 'path': None})
            else:
                return jsonify({'result': False, "error_message": 'Insufficient permissions','path':None})
        else:
            return jsonify({'result': False, "error_message": 'Project not exist','path':None})
    else:
        return jsonify({'result': False, "error_message": 'token not exist','path':None})



# 本地API—— Download-request
@app.route('/api/Download-request', methods=['GET'])
def download_request():

    token=request.args.get('token')
    Project_name=request.args.get('project_name')
    task_name=request.args.get('task_name')



    # 检查请求来源是否是本地
    if request.remote_addr != '127.0.0.1':
        abort(403)  # 403错误：权限不足

    if check_token_exists(token):

        user = get_username_by_token(token)
        projects=get_projects_by_username(user)

        if Project_name in projects:
            tasks=get_tasks_by_project(Project_name)

            if task_name in tasks:
                task = ProjectTask.query.filter_by(TaskName=task_name).first()
                return jsonify({'result': True, 'error_message': None, 'path': task.TaskPath})
            else:
                return jsonify({'result': False, "error_message": 'Task not exist','path':None})
        else:
            return jsonify({'result': False, "error_message": 'Project not exist','path':None})
    else:
        return jsonify({'result': False, "error_message": 'token not exist','path':None})





        



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
