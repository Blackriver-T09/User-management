import requests

def update_credits(token, credits_needed):
    url = 'http://127.0.0.1:5000/api/Update-credits'
    
    # 需要发送到API的数据
    data = {
        'token': token,
        'credits': credits_needed
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, json=data, headers=headers)
        
        # 检查请求是否成功
        if response.status_code == 200:
            try:
                result = response.json()
                return result
            except ValueError:                  # JSON 解析失败
                print("Failed to parse response as JSON.")
                return None
        else:               # 处理失败的响应
            print(f"Failed to check credits. Status code: {response.status_code}, Response: {response.text}")
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
    # 示例用法
    token = "k!*ijl?jfx88hl!4cyadxt2bfa*chc"
    credits_needed = 1000     #设置为负数时为加上点数
    result = update_credits(token, credits_needed)
    if result:
        print("API Call Result:", result)