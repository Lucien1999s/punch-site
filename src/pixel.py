import requests

def get_pixel_art(name):
    url = f"https://api.dicebear.com/6.x/pixel-art/svg?seed={name}"
    resp = requests.get(url)
    return resp.content.decode('utf-8')
