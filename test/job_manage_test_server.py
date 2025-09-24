from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

AUTH_KEY = "your_secret_key"

@app.route("/api/delete-task-path", methods=["POST"])
def delete_task_path():
    data = request.get_json()
    task_path_encoded = data.get("task_path")


    try:
        task_path = base64.b64decode(task_path_encoded).decode("utf-8")  # 解码任务路径
        print(f"Received task delete request for task_path: {task_path}")


        return jsonify({"success": True, "message": f"Task path '{task_path}' processed successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
