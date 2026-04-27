import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

# 读取百炼配置
BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")
BAILIAN_APP_ID = os.getenv("BAILIAN_APP_ID")
BAILIAN_URL = "https://dashscope.aliyuncs.com/api/v1/apps/completion"

# 前端页面
@app.get("/", response_class=HTMLResponse)
async def index():
    html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>家电智能客服</title>
    <style>
        body{max-width:600px;margin:20px auto;font-family:Arial}
        .chat-box{border:1px solid #ddd;padding:15px;height:400px;overflow-y:auto;margin-bottom:10px;border-radius:8px}
        .msg{margin:8px 0;padding:8px 12px;border-radius:10px}
        .user{background:#007bff;color:white;text-align:right}
        .bot{background:#f1f1f1;color:#333}
        input{width:75%;padding:10px;border-radius:8px;border:1px solid #ddd}
        button{width:20%;padding:10px;background:#007bff;color:white;border:none;border-radius:8px}
    </style>
</head>
<body>
    <h2>🏠 家护家电智能客服</h2>
    <div class="chat-box" id="chat"></div>
    <input id="input" placeholder="输入问题..." />
    <button onclick="send()">发送</button>

    <script>
        async function send() {
            let msg = document.getElementById("input").value.trim();
            if(!msg) return;
            let chat = document.getElementById("chat");
            chat.innerHTML += `<div class='msg user'>${msg}</div>`;
            document.getElementById("input").value = "";

            let res = await fetch("/chat", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({message:msg})
            });
            let data = await res.json();
            chat.innerHTML += `<div class='msg bot'>${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
    """
    return html

# 后端对接百炼知识库
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {BAILIAN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "app_id": BAILIAN_APP_ID,
        "input": {
            "prompt": user_msg
        }
    }

    try:
        response = requests.post(BAILIAN_URL, headers=headers, json=payload)
        res_json = response.json()
        reply = res_json["output"]["text"]
    except:
        reply = "服务暂时不可用"

    return {"reply": reply}