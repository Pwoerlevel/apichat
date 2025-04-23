from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import re  # لاستخراج الرقم من النص

app = FastAPI()

# إضافة CORSMiddleware للسماح بالطلبات من أي مصدر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calories")
async def get_calories(request: Request):
    # قراءة البيانات الواردة من الطلب
    data = await request.json()
    messages = data.get("messages", [])

    if not messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    # دمج الرسائل في نص واحد
    user_text = " ".join([message["content"] for message in messages])

    # إرسال النص إلى الرابط الخارجي (API)
    external_url = f"https://text.pollinations.ai/رقم فقط الرقم سعرة حرارية فقط رقم فقط رقم بدون اي كلام لي {user_text}"

    try:
        async with httpx.AsyncClient() as client:
            # إرسال طلب إلى API الخارجي
            response = await client.get(external_url)
            response.raise_for_status()  # تحقق من حالة الاستجابة

            # استخراج الرقم من النص (السعرات الحرارية)
            calories = extract_calories(response.text)
            if calories is None:
                raise HTTPException(status_code=500, detail="لم يتم العثور على السعرات الحرارية في الرد.")

            return JSONResponse(content={"calories": calories})

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"خطأ في الاتصال بـ {external_url}: {str(e)}")

# دالة لاستخراج الرقم من النص
def extract_calories(text: str) -> int:
    # استخدام تعبير منتظم لاستخراج الرقم (السعرات الحرارية)
    match = re.search(r"\d+", text)
    if match:
        return int(match.group())  # إرجاع الرقم فقط
    return None
