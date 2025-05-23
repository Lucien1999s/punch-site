import random
import requests
import time
import uuid


def get_new_token(uno, acc, pwd):
    """Get new token with error handling."""
    url = "https://pro.104.com.tw/prohrm/api/login/token"
    data = {
        "uno": uno,
        "acc": acc,
        "pwd": pwd,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOiJhcHAtcHJvZCIsImNpZCI6MCwiaWF0IjoxNTUzNzUzMTQwfQ.ieJiJtNsseSO5fxNH1XTa6bqHZ0zUyoPVUYPNtOj4TM",
    }
    resp = requests.post(url, data=data)

    # 檢查 HTTP 狀態碼
    if resp.status_code != 200:
        raise Exception(f"Login failed: {resp.status_code} - {resp.text}")

    # 嘗試解析 JSON
    try:
        resp_data = resp.json()
    except ValueError:
        raise Exception(f"Response not in JSON format: {resp.text}")

    # 檢查欄位是否存在
    if "data" not in resp_data or "access" not in resp_data["data"]:
        raise Exception(f"Unexpected response format: {resp_data}")

    # 回傳 access token
    return resp_data["data"]["access"]


def punch(uno, acc, pwd):
    """Punch with gps."""
    print(f"Data: {uno}, {acc}, {pwd}")
    time.sleep(random.randint(1, 5))
    auth_token = get_new_token(uno, acc, pwd)
    url = "https://pro.104.com.tw/prohrm/api/app/card/gps"
    if uno == "16351396":
        lat = 25.0051296
        lon = 121.2171766
    else:
        lat = random.uniform(25.0578304, 25.0584464)
        lon = random.uniform(121.5342305, 121.5349235)
    data = {
        "deviceId": str(
            uuid.uuid5(uuid.NAMESPACE_DNS, acc)
        ).upper(),  # Generate deveice id
        "latitude": lat,
        "longitude": lon,
    }
    headers = {"Authorization": "Bearer " + auth_token}
    resp = requests.post(url, data=data, headers=headers)
    return resp.status_code
