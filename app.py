from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI()

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

    food_name = user_messages[0]["content"]
    if not food_name:
        raise HTTPException(status_code=400, detail="الرجاء إرسال اسم أكلة.")

    # طلب إلى openai-reasoning API
    api_url = f"https://text.pollinations.ai/{food_name}"

    try:
        # إرسال طلب GET إلى API
        response = requests.get(api_url)

        if response.status_code != 200:
            raise Exception("فشل في الاتصال بالخدمة")

        full_content = response.text.strip()

        # نحاول استخراج رقم فقط
        match = re.fullmatch(r"\d+", full_content)
        if match:
            return PlainTextResponse(content=match.group())
        else:
            return PlainTextResponse(content="خطأ: الرجاء كتابة اسم أكلة")

    except Exception as e:
        return PlainTextResponse(content="خطأ: الرجاء كتابة اسم أكلة")
