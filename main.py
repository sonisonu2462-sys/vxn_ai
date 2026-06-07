from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# 🔑 PUT YOUR OPENAI KEY HERE
openai.api_key = "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"


@app.route("/generate", methods=["POST"])
def generate():

    data = request.json
    topic = data.get("topic")
    mode = data.get("mode")

    # ---------------- AI PROMPTS ----------------

    if mode == "study":
        prompt = f"""
Create simple STUDY NOTES for students on: {topic}

Include:
- Simple definition
- Key points
- Exam important points
- Easy explanation in Indian student style
"""

    elif mode == "ppt":
        prompt = f"""
Create PPT CONTENT for: {topic}

Format:
Slide 1: Title
Slide 2: Introduction
Slide 3: Main points
Slide 4: Examples
Slide 5: Conclusion
"""

    elif mode == "code":
        prompt = f"""
Generate Python or Arduino CODE for: {topic}

Also explain step by step in simple language.
"""

    elif mode == "deep":
        prompt = f"""
Give FULL DEEP PROJECT for: {topic}

Include:
- Full explanation
- PPT content
- PDF style notes
- Code (if needed)
- Viva questions
- Real life examples
"""

    else:
        prompt = f"Explain {topic}"

    # ---------------- OPENAI CALL ----------------

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response["choices"][0]["message"]["content"]

    return jsonify({"result": result})


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
