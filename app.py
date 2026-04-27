import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# استخدام المفتاح مباشرة لضمان التشغيل الفوري
client = OpenAI(
    api_key="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"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد نفسي إيجابي، ترد بلطف ودعم وتحفيز وتساعد الناس على التفكير بشكل أفضل."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply_content = response.choices.message.content

        # الحل السحري: بنبعت الرد بـ 3 أسماء مختلفة عشان نضمن إن الـ HTML يشوفه
        return jsonify({
            "reply": reply_content,
            "response": reply_content,
            "message": reply_content
        })

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"reply": f"عذراً، حدث خطأ فني: {str(e)}", "response": "خطأ"}), 500

if __name__ == "__main__":
    app.run(debug=True)
