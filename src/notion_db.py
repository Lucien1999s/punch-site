import json
import requests

notion_token = "secret_WHtHcPBxmpg3puyjKw672ER7YwYqBhzb8luZDNBJ2Tc"
page_id = "1ffd91e9d05c41a1a2fffb54150b758f"

def _get_blocks():
    """獲取頁面中的所有block id"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-02-22"
    }
    response = requests.get(url, headers=headers)
    json_object = response.json()
    block_ids = []
    for block in json_object["results"]:
        block_id = block["id"]
        block_ids.append(block_id)
    return block_ids

def create(user_info):
    """新建帳號"""
    infos = fetch()
    for info in infos:
        if user_info[0] == info[0]:
            return 400
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {
        "children": [
            {
                "type": "table",
                "table": {
                    "table_width": 5,                    
                    "has_column_header": True,
                    "has_row_header": False,
                    "children":[
                        {                            
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text","text": {"content": user_info[0]}}],
                                    [{"type": "text","text": {"content": user_info[1]}}],
                                    [{"type": "text","text": {"content": user_info[2]}}],
                                    [{"type": "text","text": {"content": user_info[3]}}],
                                    [{"type": "text","text": {"content": user_info[4]}}],                                   
                                ]
                            }                                
                        },                        
                    ]
                }
            }
        ]
    }
    response = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers, json=data)
    return 200

def delete(name):
    """根據帳號名稱刪除指定帳號"""
    data = fetch()
    for user_info in data:
        if user_info[0] == name:
            url = f"https://api.notion.com/v1/blocks/{user_info[-1]}"
            headers = {
                "Authorization": f"Bearer {notion_token}",
                "Notion-Version": "2022-06-28"
            }
            response = requests.delete(url=url, headers=headers)
            return response.status_code
    return None


def fetch():
    """獲取頁面中所有筆資料"""
    blocks = _get_blocks()
    res = []
    for block_id in blocks:
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        url = f"https://api.notion.com/v1/blocks/{block_id}/children"

        response = requests.get(url=url, headers=headers)
        data = json.loads(response.text)
        content_list = []
        for result in data['results']:
            for cell in result['table_row']['cells']:
                for item in cell:
                    content_list.append(item['text']['content'])
        content_list.append(block_id)
        res.append(content_list)
    res = [item for item in res if len(item) == 6]
    return res

def fetch_user(account, login_password):
    """登入用"""
    infos = fetch()
    for info in infos:
        if info[0] == account and info[1] == login_password:
            return info
    return None

def fetch_2(account):
    """帳號取資料"""
    infos = fetch()
    for info in infos:
        if info[0] == account:
            return info
    return None

if __name__ == "__main__":
    # user_info = ["ting","ting","54837596","lucien@dailyview.tw","829ptkzzZ"]
    # resp = create(user_info)
    # resp = delete("ting")
    resp = fetch()
    print(resp)