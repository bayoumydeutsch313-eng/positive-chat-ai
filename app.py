import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# الربط بالمفتاح اللي أنت حطيته في Render بأمان
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # قراءة البيانات المبعوتة من الصفحة
        data = request.get_json()
        user_message = data.get("message") or data.get("user_input")

        if not user_message:
            return jsonify({"reply": "لم تصلني رسالة، جرب مرة أخرى."}), 400

        # طلب الرد من الذكاء الاصطناعي
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد نفسي إيجابي وداعم جداً."},
                {"role": "user", "content": user_message}
            ]
        )

        # السطر ده هو "حل اللغز" اللي كان جايب الخطأ الأخير
        # لازم نضيف عشان نحدد أول رد من القائمة
        reply_content = response.choices.message.content

        # الرد بكل الأسامي الممكنة عشان يرضي ملف الـ HTML عندك
        return jsonify({
            "reply": reply_content,
            "response": reply_content,
            "message": reply_content
        })

    except Exception as e:
        # لو حصل أي حاجة تانية، السيرفر هيقولك هي إيه بالظبط
        print(f"Detailed Error: {str(e)}")
        return jsonify({"reply": f"حدث خطأ فني: {str(e)}", "response": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
