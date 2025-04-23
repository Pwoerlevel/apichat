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

@app.post("/calories")
async def get_calories(request: Request):
    data = await request.json()
    food = data.get("food")

    if not food:
        raise HTTPException(status_code=400, detail="يرجى إرسال اسم الأكلة في المفتاح 'food'.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت خبير تغذية. عندما يتم إعطاؤك اسم أكل، أرجع فقط عدد السعرات الحرارية كرقم بدون أي كلام."},
                {"role": "user", "content": f"كم عدد السعرات الحرارية في {food}؟"},
            ],
            stream=False,
            web_search=False
        )
        content = response.choices[0].message.content.strip()
        return {"calories": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
