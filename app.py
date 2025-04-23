from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# السماح بطلبات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calories")
async def get_calories(request: Request):
    data = await request.json()
    food = data.get("food", "").strip()

    if not food:
        raise HTTPException(status_code=400, detail="الرجاء إرسال اسم الأكلة")

    # بناء نص البرومبت
    prompt = f"كم عدد السعرات الحرارية في {food}؟ أجب فقط برقم السعرات بدون شرح"
    
    # استخدام API Pollinations
    url = f"https://text.pollinations.ai/{prompt}"

    async def generate_response():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()  # التأكد من أن الاستجابة كانت صحيحة
                return response.text.strip()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"حدث خطأ في الاتصال: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"حدث خطأ في الاستجابة: {e}")

    # نحصل على الرد من API
    response_text = await generate_response()
    return {"calories": response_text}
