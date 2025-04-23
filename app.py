from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FoodRequest(BaseModel):
    food: str

@app.post("/calories")
async def get_calories(data: FoodRequest):
    prompt = f"كم عدد السعرات الحرارية في {data.food}؟ أجب فقط بالرقم بدون شرح."

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openrouter.ai/v1/chat/completions",  # مثال على endpoint
            headers={
                "Authorization": "Bearer sk-xxx",  # مفتاح API الخاص بك
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-reasoning-large",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return {"calories": answer.strip()}
