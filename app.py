import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# استخدام المفتاح مباشرة لقطع أي شك في الإعدادات
# ملاحظة: إذا قمت بتغيير المفتاح في OpenAI، استبدله هنا
client = OpenAI(
    api_key="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"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # بيحاول يقرأ البيانات بأي شكل مبعوتة بيه
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        # بيشوف لو الرسالة مبعوتة باسم message أو user_input أو text
        user_message = data.get("message") or data.get("user_input") or data.get("text")

        if not user_message:
            return jsonify({"response": "لم أستلم رسالة، حاول مرة أخرى."}), 400

        # طلب الرد من OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد نفسي إيجابي، ترد بلطف ودعم وتحفيز."},
                {"role": "user", "content": user_message}
            ]
        )

        reply_content = response.choices.message.content

        # بنبعت الرد بكل الأسامي الممكنة عشان يشتغل مع أي كود HTML
        return jsonify({
            "reply": reply_content,
            "response": reply_content,
            "message": reply_content,
            "content": reply_content
        })

    except Exception as e:
        # لو حصل أي خطأ هيظهر لك هنا
        error_msg = str(e)
        print(f"Error: {error_msg}")
        return jsonify({"response": f"حدث خطأ: {error_msg}", "reply": "خطأ"}), 500

if __name__ == "__main__":
    app.run(debug=True)