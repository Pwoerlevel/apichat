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
    # استخراج البيانات المرسلة في الطلب
    data = await request.json()
    user_messages = data.get("messages", [])

    # التحقق من أن الرسالة موجودة
    if not user_messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    food_name = user_messages[0].get("content", "").strip()
    if not food_name:
        raise HTTPException(status_code=400, detail="الرجاء إرسال اسم أكلة.")

    # إعداد النص الذي سيتم إرساله إلى API
    prompt_text = f"السعرات الحرارية لي {food_name} فقط ارجع رقم فقط"

    # نقوم بترميز النص ليكون صالحًا في URL
    encoded_prompt = quote_plus(prompt_text)

    # إعداد URL API
    api_url = f"https://text.pollinations.ai/{encoded_prompt}"

    try:
        # إرسال طلب GET إلى API
        response = requests.get(api_url)

        # التحقق من حالة الاستجابة
        if response.status_code != 200:
            raise Exception(f"فشل في الاتصال بالخدمة، حالة الاستجابة: {response.status_code}")

        # استخراج النص الكامل من الاستجابة
        full_content = response.text.strip()

        # محاولة استخراج رقم فقط من النص
        match = re.fullmatch(r"\d+", full_content)
        if match:
            return PlainTextResponse(content=match.group())
        else:
            return PlainTextResponse(content="خطأ: لم أتمكن من استخراج السعرات، تأكد من صحة اسم الأكلة.")

    except Exception as e:
        # التعامل مع أي استثناءات تحدث أثناء الاتصال بـ API
        return PlainTextResponse(content=f"خطأ: لم يتمكن النظام من الاتصال بالخدمة. {str(e)}")
