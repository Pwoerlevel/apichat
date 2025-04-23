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
        "أنت خبير تغذية محترف. مهمتك الوحيدة هي إعطاء عدد السعرات الحرارية الموجودة في أكلة واحدة فقط "
        "بصورة رقمية فقط، بدون أي شرح أو كلام إضافي.\n"
        "إذا لم تكن الرسالة عبارة عن اسم أكلة أو لم تكن مفهومة، لا ترد بأي شيء."
    )
}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_messages = data.get("messages", [])

    if not user_messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    # نضيف توجيه النظام
    messages = [SYSTEM_PROMPT] + user_messages

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=False,
            web_search=False
        )
        full_content = response.choices[0].message.content.strip()

        # نحاول استخراج الرقم فقط
        match = re.search(r"\d+", full_content)
        if match:
            return PlainTextResponse(content=match.group())
        else:
            return PlainTextResponse(content="")  # لا شيء إذا ما فيه رقم
    except Exception as e:
        return PlainTextResponse(content="", status_code=500)
