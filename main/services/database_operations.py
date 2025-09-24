from sqlalchemy.exc import SQLAlchemyError
from database import *




def check_user_exists(username):
    try:
        user = User.query.filter_by(Username=username).first()
        return bool(user)  # 用户存在返回True，不存在返回False
    except SQLAlchemyError as e:
        # 处理可能的数据库查询错误
        print(f"Database error occurred: {e}")
        return None  # 数据库错误时返回None
    
def check_email_exists(email):
    try:
        user = User.query.filter_by(Email=email).first()
        return bool(user)  # 邮箱存在返回True，不存在返回False
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
                "Organization": user.Organization,
                'Credits':user.Credits,
                 
                'FirstName':user.FirstName,
                'LastName':user.LastName,
                'Gender':user.Gender,
                'Country':user.Country,
                'Affiliation':user.Affiliation,
                'ResearchArea':user.ResearchArea,


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






def get_tasks_by_project(user_id, project_name):
    try:
        # 首先获取特定用户下的特定项目
        project = UserProject.query.filter_by(ProjectName=project_name, user_id=user_id).first()
        if project:
            # 获取该项目下所有任务
            tasks = ProjectTask.query.filter_by(user_project_id=project.UserProjectId).all()
            return tasks  # 直接返回任务对象列表，而不是仅任务名称列表
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving tasks by project: {e}")
    return None  # 如果发生错误或找不到项目，返回 None


def get_user_id_by_token(token):
    try:
        # 使用 token 查询 Token 表，获取与之关联的 user_id
        token_record = Token.query.filter_by(Token=token).first()
        if token_record:
            return token_record.user_id  # 返回与令牌关联的用户 ID
        return None  # 如果找不到令牌，返回 None
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving user ID by token: {e}")
        return None  # 处理可能的数据库查询错误







def get_username_by_tokenTmp(tokenTmp):
    try:
        # 查询 TokenTmp 表以获取与 temp_token 相关联的用户
        token_record = TokenTmp.query.filter_by(tempToken=tokenTmp).first()
        
        if token_record:
            # 如果找到了 token 记录，使用 userId 来获取用户名
            user = User.query.get(token_record.userId)
            if user:
                return user.Username
            else:
                return "user not exist"
        else:
            return "token out of date"
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving tasks by project: {e}")




def verify_user_email(username, email):
    try:
        # 查询数据库中是否存在匹配的用户名和邮箱
        user = User.query.filter_by(Username=username, Email=email).first()
        if user:
            return True  # 用户名和邮箱匹配
        else:
            return False  # 用户名和邮箱不匹配
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return None  # 发生数据库错误，无法验证
    




def get_credits_by_token(token_value):
    try:
        # 通过 token 查询用户
        token = Token.query.filter_by(Token=token_value).first()   #获取第一条记录
        if token:
            user = User.query.filter_by(UserId=token.user_id).first()
            if user:
                return {
                    'status': True,
                    'credits': user.Credits,
                    'error message': None
                }
        return {
            'status': False,
            'credits': None,
            'error message': 'Token not found or invalid.'
        }
    except SQLAlchemyError as e:
        print(f"Database error occurred when retrieving credits by token: {e}")
        return {
            'status': False,
            'credits': None,
            'message': 'Database error.'
        }





def get_task_status_by_path(task_path):
    try:
        # 通过 TaskPath 查询 TaskStatus 对象
        task_status = TaskStatus.query.filter_by(TaskPath=task_path).first()
        return task_status    #注意这里返回的是一个对象
    except SQLAlchemyError as e:
        # 处理可能的数据库查询错误
        print(f"Database error occurred when retrieving task status by path: {e}")
        return None





def get_projects_and_tasks_by_username(username):
    try:
        user = User.query.filter_by(Username=username).first()
        if not user:
            return None
        
        projects = UserProject.query.filter_by(user_id=user.UserId).all()     #该用户下的所有project
        project_list = []
        
        for project in projects:
            tasks = ProjectTask.query.filter_by(user_project_id=project.UserProjectId).all()    #某个project下的所有task
            task_list = []
            
            for task in tasks:
                status = TaskStatus.query.filter_by(TaskPath=task.TaskPath).first()         #用Taskpath去TaskStatus下面找
                time_info = TaskTime.query.filter_by(TaskPath=task.TaskPath).first()       # 获取任务时间信息

                task_info = {
                    'TaskName': task.TaskName,
                    'Status': status.Status if status else 'Unknown',
                    'StartDate': time_info.StartTime if time_info else 'Not Started',
                    'EndDate': time_info.EndTime if time_info and time_info.EndTime else 'Not Completed'
                }
                task_list.append(task_info)
            
            project_info = {
                'ProjectName': project.ProjectName,
                'Tasks': task_list
            }
            project_list.append(project_info)
        
        return project_list
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return None




if __name__=='__main__':
    result=get_projects_and_tasks_by_username('heihe')
    print(result)