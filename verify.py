import requests

def verify_link(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False