


import os
from app import app, db
from database import *
import subprocess

BACKUP_PATH = './reserved/rshub_backup.sql'

def init_tables():
    print("Are you sure you want to initialize the database? All data except for backup data will be irreversibly deleted!")
    choice = input("choice (n/y): ").strip().lower()

    if choice == 'n':
        print("Operation cancelled.")
        return

    with app.app_context():
        # 初始化数据库
        db.drop_all()
        db.create_all()
        print("Database table initialization completed.")

        # 检查是否存在备份文件
        if os.path.exists(BACKUP_PATH):
            merge_choice = input("Do you want to merge data from the existing backup? (n/y): ").strip().lower()
            if merge_choice == 'y':
                try:
                    merge_backup()
                    print("The backup data has been successfully merged into the database.")
                except Exception as e:
                    print(f"合并备份失败: {e}")
            else:
                print("未合并备份数据。")
        else:
            print("未检测到备份文件。")

def merge_backup():
    print(f"Merging backup data files: {BACKUP_PATH}...")
    command = f"mysql -u {app.config['MYSQL_USER']} -p{app.config['MYSQL_PASSWORD']} {app.config['MYSQL_DB']} < {BACKUP_PATH}"
    result = subprocess.run(command, shell=True, check=True)
    if result.returncode != 0:
        raise Exception("执行备份合并失败，请检查备份文件格式和 MySQL 配置。")

if __name__ == '__main__':
    init_tables()
