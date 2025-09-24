import requests
import os


PORT = os.environ.get("UM_PORT")
def request_download(token, project_name, task_name):
    # API 端点
    # url = 'http://127.0.0.1:' + str(PORT) + '/api/Download-request'
    url = 'http://127.0.0.1:5000/api/Download-request'
    
    # 查询参数
    params = {
        'token': token,
        'project_name': project_name,
        'task_name': task_name,
    }
    
    try:
        # 发送 GET 请求
        response = requests.get(url, params=params, timeout=10)  # 设置合理的超时时间
        
        # 检查请求是否成功
        if response.status_code == 200:
            try:
                # 解析 JSON 响应体
                result = response.json()
                return result
            except ValueError:
                # JSON 解析失败
                print("Failed to parse response as JSON.")
                return None
        else:
            # 处理不成功的响应
            print(f"Failed to request download. Status code: {response.status_code}, Response: {response.text}")
            return None
    
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server.")
        return None
    except requests.exceptions.Timeout:
        print("The request timed out.")
        return None
    except requests.exceptions.RequestException as e:
        # 处理其他请求相关错误
        print(f"An error occurred: {e}")
        return None


if __name__=="__main__":
    token = "k!*ijl?jfx88hl!4cyadxt2bfa*chc"
    project_name =  "Project1"
    task_name = "task3"

    result = request_download(token, project_name, task_name)
    if result:
        print("API Call Result:", result)
