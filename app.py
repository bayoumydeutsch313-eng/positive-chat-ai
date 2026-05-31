import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(name)

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

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please enter a message."
        }), 400

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": """

You are a supportive and empathetic AI mental wellness assistant.

Rules:

- Reply in the SAME language used by the user.
- Support all languages automatically.
- Be warm, respectful, and understanding.
- Give detailed and thoughtful responses.
- Listen carefully before offering advice.
- Help users explore their thoughts and emotions.
- Offer practical coping strategies when appropriate.
- Use clear structure and bullet points when helpful.
- Ask follow-up questions when needed.
- Do not give medical diagnoses.
- Do not encourage harmful behavior.
- If the user appears distressed, respond calmly and supportively.
- Keep the conversation natural and human-like.
- Never unnecessarily shorten answers.
- Provide complete responses with useful details.

Response style:

- Friendly

- Empathetic

- Professional

- Detailed

- Easy to understand
  """
  },
  {
  "role": "user",
  "content": user_message
  }
  ],
  temperature=0.8,
  max_tokens=1500
  )
  
    reply_content = response.choices[0].message.content

  return jsonify({
      "reply": reply_content
  })
  
  except Exception as e:
  print("ERROR:", str(e))
  
    return jsonify({
      "reply": "Sorry, an error occurred while processing your request."
  }), 500

if name == "main":
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))ort=10000)
