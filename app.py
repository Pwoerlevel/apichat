from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # مسموح من كل النطاقات (غير مناسب للإنتاج)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages", [])

        if not messages or "content" not in messages[0]:
            raise HTTPException(status_code=400, detail="الرجاء إرسال prompt داخل messages.")

        prompt = messages[0]["content"]
        encoded_prompt = prompt.replace(" ", "%20")

        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://text.pollinations.ai/{encoded_prompt}")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="فشل الاتصال بـ Pollinations API.")

            result_text = response.text

        return {"response": result_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في الخادم: {str(e)}")
