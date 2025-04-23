from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client
import re

app = FastAPI()
client = Client()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "أنت خبير تغذية محترف. مهمتك فقط هي إعطاء عدد السعرات الحرارية لأكلة واحدة فقط، بصيغة رقم فقط (مثل: 350). "
        "لا تكتب أي كلمة، لا شرح، لا وحدات. فقط الرقم.\n"
        "إذا لم تكن الرسالة اسم أكلة معروفة، فلا ترد بشيء أبداً."
    )
}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_messages = data.get("messages", [])

    if not user_messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    messages = [SYSTEM_PROMPT] + user_messages

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=False,
            web_search=False
        )
        full_content = response.choices[0].message.content.strip()

        # نحاول استخراج رقم فقط
        match = re.fullmatch(r"\d+", full_content)
        if match:
            return PlainTextResponse(content=match.group())
        else:
            return PlainTextResponse(content="خطأ: الرجاء كتابة اسم أكلة")

    except Exception as e:
        print(f"Error: {e}")  # طباعه الخطأ للمساعدة في التشخيص
        return PlainTextResponse(content="خطأ: الرجاء كتابة اسم أكلة")
