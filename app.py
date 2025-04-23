import httpx
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
            # دمج الرسائل في نص واحد لتكوين الـ prompt
            prompt = " ".join([msg["content"] for msg in messages])
            # إضافة تعديلات لتوضيح أننا نريد فقط السعرات الحرارية
            prompt += " كم عدد السعرات الحرارية؟"  # إضافة سؤال خاص بالسعرات الحرارية

            # استدعاء Pollinations API
            url = f"https://text.pollinations.ai/{prompt}"

            # إرسال طلب GET إلى API
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            # تحقق من نجاح الاستجابة
            if response.status_code == 200:
                content = response.text

                # استخراج السعرات الحرارية من النص
                calories = extract_calories(content)

                if calories:
                    yield f"{calories} سعرة حرارية"
                else:
                    yield "\n[خطأ]: لم يتم العثور على معلومات السعرات الحرارية."

            else:
                yield f"\n[خطأ]: استجابة غير صالحة من الخادم."

        except Exception as e:
            yield f"\n[خطأ]: {str(e)}"

    return StreamingResponse(generate_response(), media_type="text/plain")

# دالة لاستخراج السعرات الحرارية من النص
def extract_calories(content: str):
    import re
    # نبحث عن رقم يتبع كلمة "سعرة حرارية" أو ما شابه
    match = re.search(r'(\d+)\s*سعرة حرارية', content)
    if match:
        return match.group(1)
    return None
