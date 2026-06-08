from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# ✅ SAFE API KEY (from Render Environment Variables)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ---------------- HOME ----------------
@app.route("/")
def home():
    return "VXN AI Backend Running 🚀"


# ---------------- GENERATE ----------------
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        topic = data.get("topic", "")
        mode = data.get("mode", "study")

        # ---------------- MODES ----------------

        if mode == "study":
            prompt = f"""
You are a professional teacher for Indian students.

Topic: {topic}

Create STUDY NOTES:
- Simple definition
- Key points in bullets
- Exam important points
- Real-life example
- Short revision summary
"""

        elif mode == "ppt":
            prompt = f"""
You are a PowerPoint expert.

Create PPT for students.

Topic: {topic}

Rules:
- 6 to 8 slides
- Title + 3-4 bullets per slide
- Clean structure

Format:
Slide 1: Title
Slide 2: Introduction
Slide 3: Main Concept
Slide 4: Explanation
Slide 5: Examples
Slide 6: Uses
Slide 7: Conclusion
"""

        elif mode == "code":
            prompt = f"""
You are a coding teacher.

Topic: {topic}

Give:
1. Code
2. Explanation
3. Output
4. Mistakes
"""

        elif mode == "deep":
            prompt = f"""
You are an advanced AI tutor.

Topic: {topic}

Give full deep explanation:
- Concept
- Breakdown
- Applications
- Questions
- Summary
"""

        else:
            prompt = f"Explain {topic} simply"

        # ---------------- OPENAI CALL ----------------
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        return jsonify({
            "result": result,
            "mode": mode,
            "topic": topic
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
