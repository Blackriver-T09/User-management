import requests

def delete_user_test(base_url, username,token):
    """
    测试用户注销接口
    :param base_url: API的基础URL，例如 'http://127.0.0.1:5000'
    :param username: 要注销的用户名
    :return: None
    """
    url = f"{base_url}/api/delete-user"  # 假设注销接口的路径为 /api/delete-user
    payload = {
        "username": username,
        'token':token
    }
    
    try:
        # 发送 POST 请求
        response = requests.post(url, json=payload)
        
        # 检查响应状态码
        if response.status_code == 200:
            try:
                result = response.json()                  # 解析 JSON 响应体
                print(f"Response for deleting user '{username}':", result)


            except ValueError:                  # JSON 解析失败
                print("Failed to parse response as JSON.")
        else:
            print(f"Failed to delete user. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server.")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# 示例调用
if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"  # 替换为你的服务器地址
    username = "User1"  # 替换为需要测试注销的用户名
    token='3a6fb5xolo*q*#sgxt!!2r73n?$?co'
    delete_user_test(base_url, username,token)
