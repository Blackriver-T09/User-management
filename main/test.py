
import requests

# API endpoint
url = 'http://127.0.0.1:5000/api/email'

# 测试数据：替换为有效的用户名和邮箱
data = {
    'username': '陈嘉阳',
    'email': 'jiayang.23@intl.zju.edu.cn'
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 打印响应内容
print('Status Code:', response.status_code)
print('Response:', response.json())
