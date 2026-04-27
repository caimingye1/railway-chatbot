from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

# 初始化FastAPI应用
app = FastAPI()

# 配置大模型信息
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_CHAT_MODEL = "qwen-plus"
# 把你的API Key填在这里
YOUR_API_KEY = "sk-1ad8d6640edf44059ee0f95ca16ed2c7"

client = OpenAI(
    api_key=YOUR_API_KEY,
    base_url=QWEN_BASE_URL,
)

# 挂载静态文件，让前端网页能被访问
app.mount("/static", StaticFiles(directory="static"), name="static")

# 定义请求体格式
class ChatRequest(BaseModel):
    message: str

# 聊天接口：接收用户问题，返回大模型回答
@app.post("/chat")
async def chat(request: ChatRequest):
    completion = client.chat.completions.create(
        model=QWEN_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "你是星河科技的智能客服，回答用户的问题。"},
            {"role": "user", "content": request.message}
        ]
    )
    return {"reply": completion.choices[0].message.content}

# 根路径直接返回前端网页
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")