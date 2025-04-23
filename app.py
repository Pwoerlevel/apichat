from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()
# إعدادات CORS للسماح بالطلبات من جميع المصادر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    # الحصول على البيانات من الطلب
    data = await request.json()
    messages = data.get("messages", [])
    
    # التحقق من وجود الرسائل
    if not messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")
    
    # دمج الرسائل في نص واحد
    user_text = " ".join(messages)
    
    # النص المطلوب التحقق من وجوده
    required_text = "من فضلك، يجب أن يكون الرد فقط عبارة عن رقم واحد يمثل السعر الحراري، دون إضافة أي نص أو تفاصيل أخرى."
    
    # التحقق من وجود النص المطلوب
    if required_text not in user_text:
        return PlainTextResponse("يرجى إضافة الطلب بالصيغة الصحيحة 404")
    
    # تكوين الرابط الخارجي
    external_url = f"https://text.pollinations.ai/{user_text}"
    
    # إرسال طلب إلى API الخارجية باستخدام httpx
    async with httpx.AsyncClient() as client:
        try:
            # إرسال طلب GET إلى الرابط الخارجي
            response = await client.get(external_url)
            # التحقق من حالة الاستجابة
            response.raise_for_status()
            
            def generate_response():
                try:
                    # إرجاع النص من الاستجابة للمستخدم بشكل مستمر (streaming)
                    yield response.text
                except Exception as e:
                    yield f"\n[خطأ]: {str(e)}"
            
            # إرجاع الاستجابة بشكل مستمر (streaming)
            return StreamingResponse(generate_response(), media_type="text/plain")
        except httpx.RequestError as e:
            # معالجة الأخطاء في الاتصال بالخدمة الخارجية
            raise HTTPException(status_code=500, detail=f"خطأ في الاتصال بـ {external_url}: {str(e)}")
