import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# الكود بيقرأ المفتاح من Environment في Render
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
        user_message = data.get("message") or data.get("user_input")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد نفسي إيجابي وداعم."},
                {"role": "user", "content": user_message}
            ]
        )

        # التصحيح هنا: أضفنا قبل كلمة message
        reply_content = response.choices.message.content

        return jsonify({
            "reply": reply_content,
            "response": reply_content
        })

    except Exception as e:
        return jsonify({"reply": f"حدث خطأ: {str(e)}", "response": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
