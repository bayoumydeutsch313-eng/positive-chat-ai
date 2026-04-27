from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="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"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

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

    reply = response.choices[0].message.content

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(debug=True)
