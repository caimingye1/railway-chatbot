import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 用你这个知识库应用的配置
API_KEY = os.getenv("DASHSCOPE_API_KEY")
APP_ID = "69ef035f09b67baf6090e429"  # 你的知识库应用ID

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(request: Request):
    user_msg = await request.json()
    user_msg = user_msg.get("message", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 调用你的知识库应用，而不是直接调用模型
    payload = {
        "app_id": APP_ID,
        "prompt": user_msg
    }

    try:
        response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/apps/completion",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        res_json = response.json()
        reply = res_json["output"]["text"]
    except Exception as e:
        print("错误详情：", str(e))
        reply = "客服暂时无法响应，请稍后再试"

    return {"reply": reply}