import requests

def get_json(url, fallback=None):
    try:
        res = requests.get(url)
        return res.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch from {url}: {e}")
        return fallback or {}
