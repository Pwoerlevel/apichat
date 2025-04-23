from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx  # لاستخدام HTTP للاتصال بـ API الخارجي

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
    prompt = data.get("prompt", "")

    if not prompt:
        raise HTTPException(status_code=400, detail="الرجاء إرسال النص في JSON كـ 'prompt'.")

    try:
        # إرسال النص إلى الـ API الخارجي
        url = f"https://text.pollinations.ai/{encodeURIComponent('كم سعرة في رقم اجب برقم واحد فقط فقط الرقم مباشرة بدون اي كلام' + prompt)}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="حدث خطأ أثناء الاتصال بالـ API الخارجي.")
        
        # إرجاع الرد للمستخدم
        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ: {str(e)}")
