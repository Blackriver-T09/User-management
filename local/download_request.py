import requests

def request_download(token, project_name, task_name):
    # API 端点
    url = 'http://127.0.0.1:5000/api/Download-request'
    
    # 查询参数
    params = {
        'token': token,
        'project_name': project_name,
        'task_name': task_name,
        
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
    token = "9jz?!b*4dzgu#m19@kdj$s3i*lyv"
    project_name = "New Project"
    task_name = "New TaskA"

    result = request_download(token, project_name, task_name)
    if result:
        print("API Call Result:", result)
