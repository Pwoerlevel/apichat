from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx  # نستخدم httpx لعمل GET خارجي

app = FastAPI()

# CORS Middleware
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
    messages = data.get("messages", [])

    if not messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    # نأخذ آخر رسالة من المستخدم
    prompt = messages[-1]["content"]

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://text.pollinations.ai/{prompt}")

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="فشل في جلب الرد من pollinations.")

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ: {str(e)}")
