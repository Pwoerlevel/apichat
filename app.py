from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# السماح بطلبات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح بكل النطاقات
    allow_credentials=True,
    allow_methods=["*"],  # السماح بكل الطرق
    allow_headers=["*"],  # السماح بكل الهيدرات
)

@app.post("/calories")
async def get_calories(request: Request):
    data = await request.json()
    food = data.get("food", "").strip()

    if not food:
        return {"error": "يرجى كتابة اسم الأكلة"}

    # نص البرومبت
    prompt = f"كم عدد السعرات الحرارية في {food}؟ أجب فقط برقم السعرات بدون شرح"

    url = f"https://text.pollinations.ai/{prompt}"

    try:
        # إرسال طلب GET للموقع
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            # في حالة كانت الردود غير ناجحة
            response.raise_for_status()

            # إرجاع السعرات
            return {"calories": response.text.strip()}
    
    except httpx.RequestError as e:
        return {"error": f"حدث خطأ في الاتصال: {e}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"حدث خطأ في الاستجابة: {e}"}
