from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

# إنشاء تطبيق FastAPI
app = FastAPI()

# إضافة CORSMiddleware للسماح بالطلبات من أي مصدر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح لجميع النطاقات
    allow_credentials=True,
    allow_methods=["*"],  # السماح بكل الطرق مثل GET و POST
    allow_headers=["*"],  # السماح بكل رؤوس الطلبات
)

# نقطة النهاية للتفاعل مع الـ API
@app.post("/chat")
async def chat(request: Request):
    # قراءة البيانات الواردة من الطلب
    data = await request.json()
    messages = data.get("messages", [])

    # التحقق من وجود الرسائل
    if not messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    # استدعاء API Pollinations باستخدام httpx
    async def generate_response():
        try:
            # دمج الرسائل في نص واحد
            prompt = ' '.join([message['content'] for message in messages])
            # إرسال طلب GET إلى Pollinations API
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://text.pollinations.ai/{prompt}")
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                content = response.text
                yield content  # إرسال المحتوى بشكل مستمر
            else:
                yield f"\n[خطأ]: لم تتمكن من الحصول على استجابة من API"
        except Exception as e:
            yield f"\n[خطأ]: {str(e)}"

    # إرجاع الاستجابة بشكل Streaming
    return StreamingResponse(generate_response(), media_type="text/plain")
