from fastapi import FastAPI, Request
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
        return {"error": "يرجى كتابة اسم الأكلة"}

    # نص البرومبت
    prompt = f"كم عدد السعرات الحرارية في {food}؟ أجب فقط برقم السعرات بدون شرح"

    url = f"https://text.pollinations.ai/{prompt}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return {"calories": response.text.strip()}
