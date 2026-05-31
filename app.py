import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# مهم جدًا:
# لا تضع API Key داخل الكود
# ضعه فقط داخل Render -> Environment Variables
# باسم:
# OPENAI_API_KEY

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
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
            return jsonify({
                "reply": "من فضلك اكتب رسالة أولاً"
            }), 400

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
            ],
            temperature=0.7,
            max_tokens=2000
        )

        reply_content = response.choices[0].message.content

        return jsonify({
            "reply": reply_content
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "reply": f"عذراً، حدث خطأ فني: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
