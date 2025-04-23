from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client

app = FastAPI()
client = Client()

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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=False,  # إيقاف خاصية الـ streaming
            web_search=False
        )
        content = response.choices[0].message['content']  # الحصول على الرد الكامل
        return {"response": content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ: {str(e)}")
