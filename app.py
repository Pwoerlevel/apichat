from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/calories")  # ملاحظة مهمة: استخدم المسار المطابق للمسار على Vercel
async def get_calories(request: Request):
    data = await request.json()
    food = data.get("food", "").strip()

    if not food:
        return {"error": "يرجى كتابة اسم الأكلة"}

    prompt = f"كم عدد السعرات الحرارية في {food}؟ أجب فقط برقم السعرات بدون شرح"
    url = f"https://text.pollinations.ai/{prompt}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return {"calories": response.text.strip()}
    except httpx.RequestError as e:
        return {"error": f"حدث خطأ في الاتصال: {e}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"حدث خطأ في الاستجابة: {e}"}
