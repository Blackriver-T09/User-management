import requests
import base64
from threading import Thread





# 服务器信息
SERVER_URL = "http://127.0.0.1:5001/api/delete-task-path"


def delete_task_request_async(task_path):

    try:
        # 将任务路径编码为 Base64 ,确保数据在通过网络传输时不会因特殊字符而破坏协议。
        encoded_task_path = base64.b64encode(task_path.encode("utf-8")).decode("utf-8") 
        #先用utf-8编码成字节序列，然后编码成base64, 再用 utf-8 解码回字符串格式。因为构造 JSON 请求体最终需要字符串类型数据。
        payload = {"task_path": encoded_task_path}
        response = requests.post(SERVER_URL, json=payload, timeout=10)  # 设置超时时间
        
        # 检查响应
        if response.status_code == 200:
            print(f"Delete task request successfully sent for task_path: {task_path}")
            # print("Response:", response.json())
        else:
            print(f"Failed to send delete task request for task_path: {task_path}. Status Code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"Failed to send delete task request: {e}")

def delete_task_request(task_path):

    # 创建线程来异步发送删除任务请求
    thr = Thread(target=delete_task_request_async, args=[task_path])
    thr.start()



  




if __name__=="__main__":
    message='You have been successfully registered'
    delete_task_request('jiayang.23@intl.zju.edu.cn',message,1)
    # print(message)







