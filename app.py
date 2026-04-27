import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# الكود ده هيقرأ المفتاح من إعدادات Render اللي أنت لسه محدثها
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        # تقبل الرسالة بأي اسم مبعوتة بيه من الـ HTML
        user_message = data.get("message") or data.get("user_input") or data.get("text")

        if not user_message:
            return jsonify({"response": "لم تصلني رسالة"}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد نفسي إيجابي، ترد بلطف ودعم وتحفيز."},
                {"role": "user", "content": user_message}
            ]
        )

        reply_content = response.choices.message.content

        # نرد بكل الأسماء عشان الـ HTML يشوف الرد فوراً
        return jsonify({
            "reply": reply_content,
            "response": reply_content,
            "message": reply_content
        })

    except Exception as e:
        # لو حصل خطأ، هيظهر لك سببه الحقيقي في الـ Logs
        return jsonify({"reply": f"عذراً، حدث خطأ: {str(e)}", "response": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
