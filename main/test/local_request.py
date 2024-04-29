import requests


def check_username_locally(username, password, token):
    try:
        url = f'http://127.0.0.1:5000/api/check_username'
        params = {'username': username, 'password': password, 'token': token}
        response = requests.get(url, params=params)

        status_code = response.status_code
        if status_code == 200:
            value = response.json()  # 从json格式转化为字典
            return (value['result'], value['error_message'])
        else:
            print(f"Error: Received status code {status_code}")
            return None
        

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

# print(check_username_locally('heihe','1234321','qwer'))
print(check_username_locally('heihe','1234321','qwe'))




