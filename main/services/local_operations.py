from .database_operations import *
from database import *

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from flask import Flask


def update_task_status(task_path, new_job_status, app, db):
    """
    带有应用上下文的任务状态更新函数。

    参数:
        task_path (str): 任务路径。
        new_job_status (str): 新的任务状态，必须为 'in queue', 'running', 'completed', 'failed' 之一。
        app (Flask): Flask 应用实例。
        db (SQLAlchemy): 数据库实例。
    
    返回:
        dict: 包含操作结果的字典。
    """
    valid_statuses = ['in queue', 'running', 'completed', 'failed']
    if new_job_status not in valid_statuses:
        return {"result": False, "message": "new_job_status has to be one of 'in queue', 'running', 'completed', 'failed'."}

    try:
        with app.app_context():   # 使用应用上下文
            # 获取任务状态对象
            task_status = get_task_status_by_path(task_path)  # 注意：返回的是一个对象
            if task_status is None:
                return {"result": False, "message": "Invalid task path or task path does not exist."}

            # 保存旧状态，更新新状态和时间戳
            old_task_status = task_status.Status
            task_status.Status = new_job_status
            task_status.UpdatedAt = datetime.now(timezone.utc)

            # 如果状态更新为 'completed' 且之前不是 'completed'，则更新结束时间
            if new_job_status == 'completed' and old_task_status != 'completed':
                task_time = TaskTime.query.filter_by(TaskPath=task_path).first()
                if task_time:
                    task_time.EndTime = datetime.now().strftime("%Y-%m-%d %H:%M")
                else:
                    print(f"No TaskTime entry found for task path '{task_path}'.")

            # 提交更改
            db.session.commit()
            print(f"Task with path '{task_path}' has changed from '{old_task_status}' to '{new_job_status}'.")
            return {"result": True, "message": None}

    except SQLAlchemyError as e:
        with app.app_context():
            db.session.rollback()  # 回滚更改
            print(f"SQLAlchemyError during update_task_status: {e}")
            return {"result": False, "message": "Database error."}

    except Exception as e:
        print(f"Error during update_task_status: {e}")
        return {"result": False, "message": "An unexpected error occurred."}








def update_user_credits(token, credits_needed, app, db):
    """
    带有应用上下文的用户 Credits 更新函数。

    参数:
        token (str): 用户的唯一标识令牌。
        credits_needed (int): 所需消耗的积分。
        app (Flask): Flask 应用实例。
        db (SQLAlchemy): 数据库实例。
    
    返回:
        dict: 包含操作结果的字典。
    """
    try:
        with app.app_context():  # 使用应用上下文
            # 获取用户对象
            user = get_user_by_token(token)
            if not user:
                return {"result": False, "message": "Invalid token or user does not exist."}

            # 检查是否有足够的积分
            if user.Credits < credits_needed:
                return {"result": False, "message": "Insufficient credits."}

            # 扣除积分并更新数据库
            user.Credits -= credits_needed
            new_credits = user.Credits
            db.session.commit()  # 提交更改

            # 获取用户 ID 以便记录日志
            user_id = get_user_id_by_token(token)
            print(f"{datetime.now(timezone.utc)}: User ID {user_id} has successfully updated credits to {new_credits} (change size: {-credits_needed})")
            return {"result": True, "message": None}

    except SQLAlchemyError as e:
        with app.app_context():
            db.session.rollback()  # 回滚更改
            print(f"{datetime.now(timezone.utc)}: SQLAlchemyError during update_credits: {e}")
            return {"result": False, "message": "Database error."}

    except Exception as e:
        print(f"{datetime.now(timezone.utc)}: Error during update_credits: {e}")
        return {"result": False, "message": "An unexpected error occurred."}








def check_user_credits(token, credits_needed, app, db):
    """
    带有应用上下文的用户积分检查函数。

    参数:
        token (str): 用户的唯一标识令牌。
        credits_needed (int): 所需积分。
        app (Flask): Flask 应用实例。
        db (SQLAlchemy): 数据库实例。
    
    返回:
        dict: 包含检查结果的字典。
    """
    if token is None:
        return {'logic': False, 'message': 'Please provide a token'}

    if credits_needed is None:
        return {'logic': False, 'message': 'Please provide the number of credits required'}

    try:
        with app.app_context():  # 使用应用上下文
            # 获取用户积分
            response = get_credits_by_token(token)
            status = response.get('status', False)
            credits = response.get('credits', 0)
            error_message = response.get('error message', 'Cannot retrieve response when checking credits')

            if status:
                if credits >= int(credits_needed):
                    # 获取用户 ID 并记录日志
                    user_id = get_user_id_by_token(token)
                    print(f"{datetime.now(timezone.utc)}: User ID {user_id} successfully checked credits. "
                          f"Remaining: {credits}, Required: {credits_needed}, Access granted.")
                    return {'logic': True, 'message': None}
                else:
                    user_id = get_user_id_by_token(token)
                    print(f"{datetime.now(timezone.utc)}: User ID {user_id} successfully checked credits. "
                          f"Remaining: {credits}, Required: {credits_needed}, Access denied.")
                    return {'logic': False, 'message': 'Insufficient remaining credits'}
            else:
                user_id = get_user_id_by_token(token)
                print(f"{datetime.now(timezone.utc)}: User ID {user_id} failed to check credits. "
                      f"Reason: {error_message}")
                return {'logic': False, 'message': error_message}

    except SQLAlchemyError as e:
        print(f"{datetime.now(timezone.utc)}: SQLAlchemyError during check_credits: {e}")
        logging.error(f"SQLAlchemyError during check_credits: {e}")
        return {'logic': False, 'message': "An internal error occurred. Please try again."}

    except Exception as e:
        print(f"{datetime.now(timezone.utc)}: Error during check_credits: {e}")
        logging.error(f"Error during check_credits: {e}")
        return {'logic': False, 'message': "An unexpected error occurred. Please try again."}

