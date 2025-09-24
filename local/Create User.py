import requests

def test_register():
    # API 端点
    url = 'http://47.96.167.199:5000/register'

    # 准备注册数据
    data = {
        'username': 'User1',
        'email': 'jiayang.23@intl.zju.edu.cn',
        'institution': 'UIUC',
        'password': 'C0?gJfDpZ.7d',
        'confirm_password': 'C0?gJfDpZ.7d',
        'FirstName': 'Hei',
        'LastName': 'He',
        'Gender': 'male',
        'Country': 'Neverland',
        'Affiliation': 'Example University',
        'ResearchArea': 'Data Science'
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, json=data, headers=headers)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析 JSON 响应体
            result = response.json()
            print("API Call Result:", result)
            return result
        else:
            # 处理不成功的响应
            print(f"Failed to register. Status code: {response.status_code}, Response: {response.text}")
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

if __name__ == "__main__":
    test_result = test_register()

