import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 只保留一个变量，彻底简化！
API_KEY = os.getenv("DASHSCOPE_API_KEY")

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

    payload = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "system", "content": "你是家护家电智能客服，只回答家电相关的问题，回答要简短清晰。"},
                {"role": "user", "content": user_msg}
            ]
        }
    }

    try:
        response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        res_json = response.json()
        reply = res_json["output"]["choices"][0]["message"]["content"]
    except Exception as e:
        print("错误详情：", str(e))
        reply = "客服暂时无法响应，请稍后再试"

    return {"reply": reply}