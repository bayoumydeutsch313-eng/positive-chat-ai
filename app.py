from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# حط مفتاحك هنا مباشرة بين العلامتين عشان نقطع الشك باليقين
client = OpenAI(
    api_key="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"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد نفسي إيجابي، ترد بلطف ودعم وتحفيز."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices.message.content
        return jsonify({"response": reply, "reply": reply})

    except Exception as e:
        # السطر ده هيخلينا نشوف المشكلة بالظبط في الـ Logs بتاعة Render
        print(f"Detailed Error: {e}")
        return jsonify({"response": f"حصلت مشكلة: {str(e)}", "reply": "خطأ"})

if __name__ == "__main__":
    app.run(debug=True)