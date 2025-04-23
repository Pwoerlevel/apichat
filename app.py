from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import re
from urllib.parse import quote_plus

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_messages = data.get("messages", [])

    if not user_messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    food_name = user_messages[0]["content"]
    if not food_name:
        raise HTTPException(status_code=400, detail="الرجاء إرسال اسم أكلة.")

    # إعداد النص الذي سيتم إرساله إلى API
    prompt_text = f"السعرات الحرارية لي {food_name} فقط ارجع رقم فقط"

    # نقوم بترميز النص ليكون صالحًا في URL
    encoded_prompt = quote_plus(prompt_text)

    # إرسال الطلب إلى API
    api_url = f"https://text.pollinations.ai/{encoded_prompt}"

    try:
        # إرسال طلب GET إلى API
        response = requests.get(api_url)

        if response.status_code != 200:
            raise Exception("فشل في الاتصال بالخدمة")

        # استخراج النص الكامل من الاستجابة
        full_content = response.text.strip()

        # نحاول استخراج رقم فقط
        match = re.fullmatch(r"\d+", full_content)
        if match:
            return PlainTextResponse(content=match.group())
        else:
            return PlainTextResponse(content="خطأ: الرجاء كتابة اسم أكلة معروفة")

    except Exception as e:
        return PlainTextResponse(content="خطأ: الرجاء كتابة اسم أكلة")
