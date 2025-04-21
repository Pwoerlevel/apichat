from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
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
    try:
        data = await request.json()
        messages = data.get("messages", [])

        if not messages:
            raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=False,
            web_search=False
        )

        reply = response.choices[0].message.content
        return JSONResponse(content={"reply": reply})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
