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

def lcim_send(is_group, target, text):
    if not REAL_SEND:
        print("[模拟发送]", target, text)
        return
    tk = get_token()
    if is_group and target.isdigit():
        target = f"group-{target}"
    elif not is_group and target.isdigit():
        target = int(target)
    body = {
        "toContactId": target,
        "type": "text",
        "content": f"<p>{text}</p>"
    }
    raw = json.dumps(body).encode()
    req = urllib.request.Request(
        SEND_URL, data=raw, method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tk}"
        }
    )
    urllib.request.urlopen(req, timeout=15)

@app.route("/webhook", methods=["POST"])
def lcim_hook():
    data = request.get_json()
    if not data:
        return jsonify({"ok": False}), 400
    event = data.get("type")
    if event == "text":
        c = data.get("content", "").strip()
        sender = str(data.get("fromUser", {}).get("id"))
        is_g = data.get("is_group", False)
        if c == "/ping":
            lcim_send(is_g, sender, "pong!")
        elif c == "/help":
            lcim_send(is_g, sender, "可用指令：/ping /help")
    return jsonify({"ok": True})

def verify_gh(sig_header, body):
    if not GITHUB_WEBHOOK_SECRET or not sig_header.startswith("sha256="):
        return False
    sig = sig_header.removeprefix("sha256=")
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), body, hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), sig)

@app.route("/github", methods=["POST"])
def github_hook():
    body = request.get_data()
    sig = request.headers.get("X-Hub-Signature-256", "")
    event = request.headers.get("X-GitHub-Event", "")
    if not verify_gh(sig, body):
        return jsonify({"ok": False}), 403
    payload = json.loads(body)
    repo = payload["repository"]["full_name"]
    msg = ""
    if event == "star":
        u = payload["sender"]["login"]
        if payload["action"] == "created":
            msg = f"⭐ @{u} 给 {repo} 点了 Star！"
        else:
            msg = f"💔 @{u} 取消 Star"
    elif event == "push":
        user = payload["pusher"]["name"]
        commit_msg = payload["commits"][0]["message"]
        msg = f"📤 {user} 推送代码：\n{commit_msg}"
    if msg and NOTIFY_GROUP_ID:
        lcim_send(True, NOTIFY_GROUP_ID, msg)
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
