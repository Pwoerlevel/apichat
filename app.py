from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

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

    def generate_response():
        try:
            # استجابة ثابتة أو منطق خاص بك هنا
            response = "هذه استجابة ثابتة من الخادم!"
            yield response  # إرسال الاستجابة بشكل مستمر (stream)
        except Exception as e:
            yield f"\n[خطأ]: {str(e)}"

    return StreamingResponse(generate_response(), media_type="text/plain")
