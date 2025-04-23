from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
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

    def generate_response():
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
                web_search=False
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content  # هذه هي البيانات التي سيتم إرسالها بشكل مستمر (stream)
        except Exception as e:
            yield f"\n[خطأ]: {str(e)}"

    return StreamingResponse(generate_response(), media_type="text/plain")
