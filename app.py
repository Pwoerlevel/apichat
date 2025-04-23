from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client

# إعداد FastAPI
app = FastAPI()

# إنشاء عميل g4f
client = Client()

# إضافة Middleware للسماح بالـ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح لجميع الأصول
    allow_credentials=True,
    allow_methods=["*"],  # السماح لجميع الأساليب مثل GET, POST
    allow_headers=["*"],  # السماح بكل الرؤوس
)

# المسار الذي يستقبل الطلبات
@app.post("/chat")
async def chat(request: Request):
    # قراءة البيانات المرسلة
    data = await request.json()
    messages = data.get("messages", [])

    # التحقق من وجود الرسائل
    if not messages:
        raise HTTPException(status_code=400, detail="الرجاء إرسال الرسائل في JSON كـ 'messages'.")

    try:
        # إرسال الرسائل إلى نموذج gpt-4o-mini عبر g4f
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=False,  # تعطيل التدفق المستمر
            web_search=False
        )
        
        # إرجاع الرد للمستخدم
        return {"response": response.choices[0].text}

    except Exception as e:
        # في حالة حدوث خطأ، إرجاع رسالة خطأ للمستخدم
        raise HTTPException(status_code=500, detail=f"حدث خطأ: {str(e)}")
