import requests

def request_download(token, project_name, task_name, level_required):
    # API 端点
    url = 'http://127.0.0.1:5000/api/Download-request'
    
    # 查询参数
    params = {
        'token': token,
        'project_name': project_name,
        'task_name': task_name,
        'level': level_required  # 注意这里参数名应与API中接收的参数名一致
    }
    
    # 发送 GET 请求
    response = requests.get(url, params=params)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 JSON 响应体
        result = response.json()
        return result
    else:
        # 处理错误情况
        print(f"Failed to request download. Status code: {response.status_code}")
        return None

if __name__=="__main__":
    token = "ncc96!dks*s6sgud8n3!?r70e@6#qp"
    project_name = "New Project1"
    task_name = "New Task1"

    result = request_download(token, project_name, task_name)
    if result:
        print("API Call Result:", result)
