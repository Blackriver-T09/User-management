import requests

def manual_backup():
    url = "http://127.0.0.1:5000/manual-backup"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed to trigger manual backup. Status Code:", response.status_code)
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    manual_backup()
