from flask import Flask, request, jsonify
import os, hmac, hashlib, json, urllib.request

app = Flask(__name__)

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
REAL_SEND = os.getenv("REAL_SEND", "False") == "True"
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
NOTIFY_GROUP_ID = os.getenv("NOTIFY_GROUP_ID")

SEND_URL = "https://www.lcim.site/enterprise/im/sendMessage"
TOKEN_URL = "https://www.lcim.site/enterprise/im/auth/token"

token_cache = {"value": None, "expire": 0}

def get_token():
    import time
    now = time.time()
    if token_cache["value"] and now < token_cache["expire"] - 60:
        return token_cache["value"]
    payload = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(
        TOKEN_URL, data=payload, method="POST",
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.load(r)
        tk = data["data"]["access_token"]
        exp = data["data"]["expires_in"]
        token_cache["value"] = tk
        token_cache["expire"] = now + exp
        return tk


