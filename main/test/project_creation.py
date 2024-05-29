import requests

def create_project(token, project_name):
    # API 端点
    url = 'http://127.0.0.1:5000/api/Project-creation'
    
    # 查询参数
    params = {
        'token': token,
        'project_name': project_name
    }
    
    # 发送 GET 请求
    response = requests.get(url, params=params)
    
    # 检查请求是否成功
    if response.status_code == 200:

        result = response.json()          # 解析 JSON 响应体
        return result
    else:
        # 处理错误情况
        print(f"Failed to create project. Status code: {response.status_code}")
        return None


if __name__=="__main__":
    # 示例用法
    token = "oc40m*v55pb2*x@@7h!bin41!hwuh"
    project_name = "New Project1"
    result = create_project(token, project_name)
    if result:
        print("API Call Result:", result)
