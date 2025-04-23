from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

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
    messages = data.get("messages", [])

    if not messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    # إرسال النص إلى الرابط الخارجي
    user_text = " ".join(messages)  # دمج الرسائل (إذا كانت متعددة)
    external_url = f"https://text.pollinations.ai/{user_text}"

    async with httpx.AsyncClient() as client:
        try:
            # إرسال طلب إلى API الخارجي
            response = await client.get(external_url)
            response.raise_for_status()  # تحقق من حالة الاستجابة

            def generate_response():
                try:
                    # إرجاع الرد من الخادم الخارجي للمستخدم
                    yield response.text  # إرسال الاستجابة بشكل مستمر (stream)
                except Exception as e:
                    yield f"\n[خطأ]: {str(e)}"

            return StreamingResponse(generate_response(), media_type="text/plain")

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"خطأ في الاتصال بـ {external_url}: {str(e)}")
