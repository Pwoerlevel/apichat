from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware

# إنشاء التطبيق FastAPI
app = FastAPI()

# إضافة CORSMiddleware للسماح بالطلبات من أي مصدر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح لجميع النطاقات
    allow_credentials=True,
    allow_methods=["*"],  # السماح بكل الطرق مثل GET و POST
    allow_headers=["*"],  # السماح بكل رؤوس الطلبات
)

@app.get("/generate-text")
async def generate_text(prompt: str):
    # URL الخاص بـ API الخارجي
    external_url = f"https://text.pollinations.ai/{prompt}"

    async with httpx.AsyncClient() as client:
        # إرسال طلب GET إلى API الخارجي
        response = await client.get(external_url)
    
    # إذا كانت الاستجابة ناجحة (status code 200)
    if response.status_code == 200:
        return JSONResponse(content={"response": response.json()})
    else:
        # إذا حدث خطأ في الاستجابة
        return JSONResponse(content={"error": "Failed to fetch the response from the external API"}, status_code=500)
