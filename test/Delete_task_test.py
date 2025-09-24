import requests

def delete_task(token, project_name, task_name):
    url = "http://127.0.0.1:5000/api/delete-task"
    payload = {
        "token": token,
        "project_name": project_name,
        "task_name": task_name
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to delete task. Status Code:", response.status_code)
    except Exception as e:
        print("Error occurred:", e)

# 示例调用
if __name__=="__main__":
    delete_task("3a6fb5xolo*q*#sgxt!!2r73n?$?co", "project0", "project0 task2")
