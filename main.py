import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 读取百炼配置
BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")
BAILIAN_APP_ID = os.getenv("BAILIAN_APP_ID")
BAILIAN_URL = "https://dashscope.aliyuncs.com/api/v1/apps/completion"

# 前端页面（读取 static/index.html）
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

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