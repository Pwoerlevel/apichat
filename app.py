<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>واجهة الدردشة</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        #response {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            width: 80%;
            margin: 0 auto;
            min-height: 100px;
        }
        #chatBox {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>مرحبا بك في خدمة الدردشة</h1>
    
    <div>
        <textarea id="userInput" placeholder="اكتب رسالتك هنا..." rows="4" cols="50"></textarea>
    </div>
    <div id="chatBox">
        <button onclick="sendMessage()">إرسال</button>
    </div>

    <div id="response"></div>

    <script>
        async function sendMessage() {
            const userInput = document.getElementById('userInput').value;

            if (!userInput) {
                alert("الرجاء كتابة نص.");
                return;
            }

            // إرسال الطلب إلى الخادم
            const responseElement = document.getElementById('response');
            responseElement.innerHTML = "جاري معالجة الرسالة...";

            try {
                const response = await fetch("https://apichat-bifn8t037-pwoerlevels-projects.vercel.app/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ messages: [userInput] })
                });

                if (response.ok) {
                    const text = await response.text();
                    responseElement.innerHTML = text;
                } else {
                    responseElement.innerHTML = "حدث خطأ أثناء معالجة الرسالة.";
                }
            } catch (error) {
                responseElement.innerHTML = `خطأ في الاتصال بالخادم: ${error.message}`;
            }
        }
    </script>
</body>
</html>
