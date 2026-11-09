
import json
import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

CONTENT_TYPES = {
    "instagram": "Instagram caption",
    "linkedin": "LinkedIn post",
    "blog": "Blog introduction",
}

TONES = {
    "professional": "Professional and clear",
    "friendly": "Friendly and conversational",
    "creative": "Creative and engaging",
    "informative": "Informative and educational",
    "persuasive": "Persuasive but not pushy",
    "witty": "Light, witty, and tasteful",
}

OUTPUT_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "title": {"type": "STRING"},
        "content": {"type": "STRING"},
        "hashtags": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        "tips": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
    },
    "required": ["title", "content", "hashtags", "tips"],
}

SYSTEM_INSTRUCTION = """
You are AI Content Studio, a professional multilingual content-writing assistant.

Your job is to create original, useful and natural content based on the user's brief.

GENERAL RULES:
- Follow the requested platform, tone, audience, language and length.
- Do not invent facts, statistics, quotes or claims.
- Keep content natural, readable and grammatically correct.
- Do not put hashtags inside the main content.
- Return hashtags separately.
- Provide useful and concise publishing tips.
- All fields including title, content, hashtags and tips must follow
  the selected language, except hashtags that are proper names or
  commonly used English social media tags.

STRICT LANGUAGE RULES:

1. ENGLISH:
- Write entirely in natural English.
- Do not insert Urdu or Hindi sentences.

2. ROMAN URDU:
- Write in Pakistani Urdu using English/Roman alphabets.
- Use natural Pakistani Urdu words and expressions.
- Do not use Hindi vocabulary, Hindi translations or Indian Hindi expressions.
- Avoid words such as "aapka swagat hai", "shuruaat", "dostों",
  "bahut", "kya aap jaante hain" and similar Hindi-style expressions.
- Prefer Pakistani Urdu expressions such as:
  "khush aamdeed", "aaghaz", "doston", "bohat",
  "kya aap jaante hain".
- Use English technical terms where they are commonly used
  in the Pakistani developer community.
- Never use Urdu script or Devanagari script in Roman Urdu output.
- Do not randomly mix Hindi words into Pakistani Urdu.

3. URDU:
- Write entirely in proper Urdu script.
- Use natural Pakistani Urdu vocabulary and expressions.
- Do not use Hindi vocabulary or Devanagari script.
- English technical terms may be retained when commonly used
  in the technology field.
- Do not write Urdu sentences using English alphabets.

IMPORTANT:
The selected language is mandatory.
Do not choose a different language yourself.
Do not mix Roman Urdu and Urdu script.
Do not mix Hindi and Pakistani Urdu.
"""

@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "model": MODEL_NAME
    })


@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}

    topic = (data.get("topic") or "").strip()
    content_type = data.get("content_type", "instagram")
    tone = data.get("tone", "professional")
    audience = (data.get("audience") or "General audience").strip()
    language = (data.get("language") or "English").strip()
    length = data.get("length", "medium")
    keywords = (data.get("keywords") or "").strip()

    if len(topic) < 3:
        return jsonify({
            "error": "Please enter a topic with at least 3 characters."
        }), 400

    if len(topic) > 500:
        return jsonify({
            "error": "Topic must be 500 characters or fewer."
        }), 400

    if content_type not in CONTENT_TYPES:
        return jsonify({
            "error": "Please select a valid content type."
        }), 400

    if tone not in TONES:
        return jsonify({
            "error": "Please select a valid writing tone."
        }), 400

    if length not in {"short", "medium", "long"}:
        return jsonify({
            "error": "Please select a valid content length."
        }), 400

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "error": "Gemini API key is missing. Add GEMINI_API_KEY to your .env file and restart the server."
        }), 503

    user_prompt = f"""
Create a {CONTENT_TYPES[content_type]} about this topic:

{topic}

Audience: {audience}

Writing tone: {TONES[tone]}

SELECTED LANGUAGE: {language}

CONTENT LENGTH: {length}

Additional keywords or points:
{keywords or "No extra keywords provided."}

LANGUAGE REQUIREMENT:
The entire generated response must strictly follow the selected language.
Read and follow the language rules in your system instructions.
Do not translate the selected language into another language.

Create original, platform-appropriate content that is ready for review.
"""

    try:
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=60000)
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_json_schema=OUTPUT_SCHEMA,
                temperature=0.5,
                max_output_tokens=1200,
            ),
        )

        result = response.parsed

        if result is None:
            result = json.loads(response.text)

        if hasattr(result, "model_dump"):
            result = result.model_dump()
        elif not isinstance(result, dict):
            result = dict(result)

        result.setdefault("title", "Your generated content")
        result.setdefault("content", "")
        result.setdefault("hashtags", [])
        result.setdefault("tips", [])

        if not result["content"].strip():
            raise ValueError("The model returned empty content.")

        return jsonify({
            "result": result,
            "meta": {
                "content_type": CONTENT_TYPES[content_type],
                "tone": TONES[tone],
                "model": MODEL_NAME,
                "language": language,
            }
        })

    except json.JSONDecodeError:
        app.logger.exception("Could not parse Gemini JSON response")

        return jsonify({
            "error": "The AI returned an unexpected format. Please try again."
        }), 502

    except Exception as exc:
        app.logger.exception("Content generation failed")

        message = str(exc).lower()

        if "api key" in message or "unauthorized" in message or "permission" in message:
            friendly = "Gemini could not authenticate your API key. Check that your key is correct and enabled."

        elif "quota" in message or "rate" in message:
            friendly = "The Gemini API request limit may have been reached. Check your API usage or try again later."

        elif "503" in message or "unavailable" in message:
            friendly = "Gemini is temporarily experiencing high demand. Please try again shortly."

        elif "504" in message or "deadline" in message or "timeout" in message:
            friendly = "Gemini took too long to respond. Please try again."

        else:
            friendly = "Something went wrong while contacting Gemini. Check your internet connection and API configuration, then try again."

        return jsonify({
            "error": friendly
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
