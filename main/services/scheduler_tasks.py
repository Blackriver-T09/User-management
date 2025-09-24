from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError
from database import *


import subprocess
import os
import logging

from apscheduler.schedulers.background import BackgroundScheduler  #这个库用于设置定时任务，使tokenTmp 在创建后10分钟自动删除




# 用于生成当前时间戳
def now_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")



# 删除过期的tokenTmp
def delete_expired_tokenTmps(app,db):
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
def backup_database(app,reserve_folder_path):
    try:
        # 读取数据库配置
        db_user = app.config['MYSQL_USER']
        db_password = app.config['MYSQL_PASSWORD']
        db_name = app.config['MYSQL_DB']


    
        os.makedirs(reserve_folder_path, exist_ok=True)                            # 确保备份目录存在
        backup_path = os.path.join(reserve_folder_path, f"{db_name}_backup.sql")   #每次运行备份脚本时新的备份文件会覆盖前一次的备份文件
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
def check_db_size(app,reserve_folder_path):
    try:
        backup_path = os.path.join(reserve_folder_path, f"{app.config['MYSQL_DB']}_backup.sql")
        file_size = os.path.getsize(backup_path)

        print(f'{now_time()}: Database file size: {file_size} bytes')
        logging.info(f"Database file size: {file_size} bytes")

    except FileNotFoundError:

        print(f'{now_time()}: Backup file does not exist.')
        logging.error("Backup file does not exist.")

    except Exception as e:

        print(f'{now_time()}: Failed to check database file size: {e}')
        logging.error(f"Failed to check database file size: {e}")



# 扫描并删除24h未激活的账户
def delete_unactivated_users(app, db):
    with app.app_context():
        try:
            # 获取当前时间24小时前的时间点
            time_threshold = datetime.now() - timedelta(hours=24)
            # 查询所有未激活的用户且创建时间小于该时间阈值的用户
            unactivated_users = User.query.filter(User.Activated == False, User.createdAt < time_threshold).all()
            count = len(unactivated_users)
            for user in unactivated_users:
                db.session.delete(user)
            db.session.commit()

            print(f'{now_time()}: Deleted {count} unactivated user accounts.')
            logging.info(f"Deleted {count} unactivated user accounts.")
        except Exception as e:
            db.session.rollback()

            print(f"{now_time()}: Failed to delete unactivated user accounts: {e}")
            logging.error(f"Failed to delete unactivated user accounts: {e}")



def start_scheduler(app,db,reserve_folder_path,gap_hours):
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_tokenTmps, 
                      'interval', 
                      minutes=10,               # 保留这个任务每10分钟运行一次，以清理过期的 tokenTmp
                      args=[app,db])  
    scheduler.add_job(backup_database, 
                      'interval', 
                      hours=gap_hours, 
                      next_run_time=datetime.now() + timedelta(seconds=10),  # 10秒后开始第一次备份（next_run_time来控制首次任务执行的具体时间）
                      args=[app,reserve_folder_path])  
    scheduler.add_job(check_db_size, 
                      'interval', 
                      hours=gap_hours, 
                      next_run_time=datetime.now() + timedelta(seconds=40),   # 40秒后开始第一次文件大小检查
                      args=[app,reserve_folder_path])  
    scheduler.add_job(delete_unactivated_users, 
                      'interval', 
                      hours=24, 
                      next_run_time=datetime.now() + timedelta(seconds=20),   # 20秒后开始第一次文件大小检查
                      args=[app, db])

    scheduler.start()










