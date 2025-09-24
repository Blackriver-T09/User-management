import requests
import json

def test_profile_page(tokenTmp):
    # API 端点
    url = 'http://127.0.0.1:5000/profile'
    
    # 请求体
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({
        'tokenTmp': tokenTmp
    })
    
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=data)
        
        # 检查请求是否成功
        if response.status_code == 200:
            try:
                # 解析 JSON 响应体
                result = response.json()
                return result
            except ValueError:
                # JSON 解析失败
                print("Failed to parse response as JSON.")
                return {'result': False, 'error': 'Failed to parse JSON'}
        else:
            # 处理不成功的响应
            print(f"Failed to access profile. Status code: {response.status_code}, Response: {response.text}")
            return {'result': False, 'error': f'Response {response.status_code}: {response.text}'}
        
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server.")
        return {'result': False, 'error': 'Connection error'}
    except requests.exceptions.Timeout:
        print("The request timed out.")
        return {'result': False, 'error': 'Timeout'}
    except requests.exceptions.RequestException as e:
        # 处理其他请求相关错误
        print(f"An error occurred: {e}")
        return {'result': False, 'error': str(e)}

if __name__ == "__main__":
    # 示例用法
    tokenTmp = "k2scf40own87yqakqasvxswosdw7ke"
    result = test_profile_page(tokenTmp)
    if result:
        print("API Call Result:", result)
