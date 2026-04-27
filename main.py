import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")
BAILIAN_APP_ID = os.getenv("BAILIAN_APP_ID")
BAILIAN_URL = "https://dashscope.aliyuncs.com/api/v1/apps/completion"

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ↓↓↓ 就是这里，换成我给你的这段 ↓↓↓
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
        print("状态码：", response.status_code)
        print("返回内容：", response.text)
        res_json = response.json()
        reply = res_json["output"]["text"]
    except Exception as e:
        reply = f"错误：{str(e)}"
        print("异常信息：", e)

    return {"reply": reply}