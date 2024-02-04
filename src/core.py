import random
import requests
import time
import uuid


def get_new_token(uno, acc, pwd):
    """Get new token."""
    url = "https://pro.104.com.tw/prohrm/api/login/token"
    data = {
        "uno": uno,
        "acc": acc,
        "pwd": pwd,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOiJhcHAtcHJvZCIsImNpZCI6MCwiaWF0IjoxNTUzNzUzMTQwfQ.ieJiJtNsseSO5fxNH1XTa6bqHZ0zUyoPVUYPNtOj4TM",
    }
    resp = requests.post(url, data=data)
    auth_token = resp.json()["data"]["access"]
    return auth_token


def punch(uno, acc, pwd):
    """Punch with gps."""
    print(f"Data: {uno}, {acc}, {pwd}")
    time.sleep(random.randint(1, 5))
    auth_token = get_new_token(uno, acc, pwd)
    url = "https://pro.104.com.tw/prohrm/api/app/card/gps"
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
