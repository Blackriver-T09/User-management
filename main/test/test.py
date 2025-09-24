import sys
import os
# 此处os.path.dirname()可以获得上一级目录，也就是当前文件或文件夹的父目录
# 将目录加入到sys.path即可生效，可以帮助python定位到文件（注：这种方法仅在运行时生效，不会对环境造成污染）
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import flask
import requests
from utils import *
from services import *



if __name__=='__main__':
    result=get_projects_and_tasks_by_username('heihe')
    print(result)

