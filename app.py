import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# الربط بمفتاح OpenAI من إعدادات Render (Environment Variables)
# تأكد إنك سميت الـ Key في Render باسم OPENAI_API_KEY
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # استقبال الرسالة من المستخدم
        user_message = request.json.get("message")

        # طلب الرد من OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "أنت مساعد نفسي إيجابي، ترد بلطف ودعم وتحفيز وتساعد الناس على التفكير بشكل أفضل بدون تشخيص طبي."
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ]
        )

        # استخراج نص الرد
        reply = response.choices.message.content

        # بنبعت الرد للشاشة (HTML) بالاسمين (response و reply) 
        # عشان نضمن إنه يشتغل مهما كان الكود اللي كاتبه في الـ HTML
        return jsonify({
            "response": reply,
            "reply": reply
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "عذراً، حدث خطأ ما. حاول مرة أخرى.", "reply": "خطأ"}), 500

if __name__ == "__main__":
    app.run(debug=True)