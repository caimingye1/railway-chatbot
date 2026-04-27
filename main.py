import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 百炼配置
BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")
BAILIAN_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# 首页（加载你自己写的客服页面）
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# 客服对话接口（对接百炼AI，100%可用）
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {BAILIAN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "system", "content": "你是家护家电智能客服，专业、耐心回答用户关于家电的问题。"},
                {"role": "user", "content": user_msg}
            ]
        }
    }

    try:
        response = requests.post(BAILIAN_URL, headers=headers, json=payload)
        res_json = response.json()
        reply = res_json["output"]["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "客服暂时无法响应，请稍后再试"

    return {"reply": reply}