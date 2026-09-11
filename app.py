import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load .env file
load_dotenv(override=True)

app = Flask(__name__)

# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_MODEL = os.environ.get(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
).strip()

SYSTEM_INSTRUCTION = """
You are an AI Learning Tutor created for SDG 4: Quality Education.

Your purpose is to provide personalized learning support to students.

You must:
- Explain academic concepts clearly.
- Adapt explanations to Beginner, Intermediate, or Advanced learners.
- Give simple examples.
- Create quizzes and practice questions.
- Check student answers.
- Give constructive feedback.
- Explain mistakes and help students improve.
- Create study plans.
- Help with Python, programming, AI/ML, DBMS, mathematics,
  computer science, electronics and other academic subjects.
- Encourage learning instead of simply giving answers.
- Break difficult topics into small understandable steps.

For BEGINNER learners:
Use simple language and basic examples.

For INTERMEDIATE learners:
Use moderate technical detail and practical examples.

For ADVANCED learners:
Give deeper explanations, reasoning and challenging examples.

Always be friendly, encouraging and educational.

This application supports SDG 4 - Quality Education by making
personalized learning assistance available through AI.
"""


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_gemini_client():
    """Create and return Gemini client using API key from .env."""

    load_dotenv(override=True)

    api_key = os.environ.get(
        "GEMINI_API_KEY",
        ""
    ).strip()

    if not api_key:
        return None

    if api_key == "your_gemini_api_key_here":
        return None

    try:
        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        return client

    except Exception as error:
        print("[Gemini Client Error]", error)
        return None


# ============================================================
# GENERATE AI RESPONSE
# ============================================================

def generate_ai_response(
    user_input,
    learner_level="Beginner",
    mode="learn"
):
    """Generate response from Google Gemini."""

    client = get_gemini_client()

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    if client is None:
        return (
            "🔑 **Gemini API Key Required**\n\n"
            "Please add your Gemini API key to the `.env` file.\n\n"
            "Example:\n"
            "`GEMINI_API_KEY=your_actual_api_key`"
        )

    # --------------------------------------------------------
    # LEARNER LEVEL
    # --------------------------------------------------------

    level_instruction = {

        "Beginner":
            """
Explain using very simple language.
Use easy examples and explain step by step.
Avoid unnecessary technical terms.
""",

        "Intermediate":
            """
Explain with moderate technical detail.
Use practical examples and some technical terminology.
""",

        "Advanced":
            """
Explain with deeper technical detail.
Include reasoning, technical concepts and challenging examples.
"""
    }

    # --------------------------------------------------------
    # LEARNING MODE
    # --------------------------------------------------------

    mode_instruction = {

        "learn":
            """
Teach and explain the student's topic clearly.
Break the topic into understandable steps.
""",

        "quiz":
            """
Create a short quiz appropriate for the learner level.

Include 5 questions.
Use a mixture of multiple-choice and short-answer questions.

Do NOT reveal the answers immediately.
Ask the student to answer first.
""",

        "feedback":
            """
Evaluate the student's answer.

Tell the student whether the answer is:
- Correct
- Partially correct
- Incorrect

Explain why and show how the answer can be improved.
""",

        "study_plan":
            """
Create a practical study plan.

Include:
- Topics
- Daily tasks
- Practice activities
- Revision
- Small goals

Keep the plan realistic for a college student.
"""
    }

    # --------------------------------------------------------
    # FINAL PROMPT
    # --------------------------------------------------------

    prompt = f"""
Learner Level:
{learner_level}

Learning Mode:
{mode}

Learner Instructions:
{level_instruction.get(
    learner_level,
    level_instruction["Beginner"]
)}

Learning Task:
{mode_instruction.get(
    mode,
    mode_instruction["learn"]
)}

Student Message:
{user_input}

Important:
- Be educational.
- Be friendly.
- Be clear.
- Use headings when useful.
- Use bullet points when useful.
- Give examples.
- Do not make the explanation unnecessarily complicated.
"""

    # --------------------------------------------------------
    # CALL GEMINI API
    # --------------------------------------------------------

    try:

        from google.genai import types

        config = types.GenerateContentConfig(

            system_instruction=SYSTEM_INSTRUCTION,

            temperature=0.7,

            max_output_tokens=1200
        )

        model_name = os.environ.get(
            "GEMINI_MODEL",
            GEMINI_MODEL
        ).strip()

        response = client.models.generate_content(

            model=model_name,

            contents=prompt,

            config=config
        )

        if response and response.text:

            return response.text.strip()

        return (
            "I couldn't generate a response right now. "
            "Please try again. 😊"
        )

    # --------------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------------

    except Exception as error:

        error_message = str(error)

        print("[Gemini API Error]", error_message)

        # Rate limit
        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):

            return (
                "⏳ **API Limit Reached**\n\n"
                "The Gemini API has temporarily reached its usage limit.\n\n"
                "Please wait for a while and try again."
            )

        # Invalid API key
        if (
            "API_KEY_INVALID" in error_message
            or "INVALID_ARGUMENT" in error_message
            or "PERMISSION_DENIED" in error_message
            or "403" in error_message
        ):

            return (
                "❌ **Invalid Gemini API Key**\n\n"
                "Please check your `GEMINI_API_KEY` "
                "inside the `.env` file."
            )

        # Model not found
        if (
            "404" in error_message
            or "NOT_FOUND" in error_message
        ):

            return (
                f"⚠️ **Model Not Found**\n\n"
                f"The model `{model_name}` could not be found.\n\n"
                "Please check the `GEMINI_MODEL` value "
                "inside your `.env` file."
            )

        # Connection error
        if (
            "connection" in error_message.lower()
            or "timeout" in error_message.lower()
        ):

            return (
                "🌐 **Connection Problem**\n\n"
                "Unable to connect to the Gemini AI service.\n"
                "Please check your internet connection and try again."
            )

        # General error
        return (
            "⚠️ **Gemini AI Error**\n\n"
            "The AI service could not complete your request.\n\n"
            "Please try again after a moment."
        )


# Compatibility name
get_bot_response = generate_ai_response


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# CHAT API
# ============================================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        # ----------------------------------------------------
        # MESSAGE
        # ----------------------------------------------------

        message = data.get(
            "message",
            ""
        ).strip()

        # ----------------------------------------------------
        # LEVEL
        # ----------------------------------------------------

        level = data.get(
            "level",
            "Beginner"
        )

        if isinstance(level, str):
            level = level.strip()

        # ----------------------------------------------------
        # MODE
        # ----------------------------------------------------

        mode = data.get(
            "mode",
            "learn"
        )

        if isinstance(mode, str):
            mode = mode.strip()

        # ----------------------------------------------------
        # EMPTY MESSAGE
        # ----------------------------------------------------

        if not message:

            return jsonify({

                "status": "error",

                "message":
                    "Please enter a question."

            }), 400

        # ----------------------------------------------------
        # VALIDATE LEVEL
        # ----------------------------------------------------

        valid_levels = [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]

        if level not in valid_levels:

            level = "Beginner"

        # ----------------------------------------------------
        # VALIDATE MODE
        # ----------------------------------------------------

        valid_modes = [
            "learn",
            "quiz",
            "feedback",
            "study_plan"
        ]

        if mode not in valid_modes:

            mode = "learn"

        # ----------------------------------------------------
        # GENERATE RESPONSE
        # ----------------------------------------------------

        reply = generate_ai_response(
            message,
            level,
            mode
        )

        # ----------------------------------------------------
        # SEND RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "status": "success",

            "reply": reply,

            "timestamp":
                datetime.now().strftime(
                    "%I:%M %p"
                ),

            "level": level,

            "mode": mode
        })

    except Exception as error:

        print(
            "[Server Error]",
            error
        )

        return jsonify({

            "status": "error",

            "message":
                "Something went wrong. Please try again."

        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    api_key = os.environ.get(
        "GEMINI_API_KEY",
        ""
    ).strip()

    return jsonify({

        "status": "online",

        "gemini_configured":
            bool(api_key),

        "model":
            os.environ.get(
                "GEMINI_MODEL",
                GEMINI_MODEL
            )
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    api_key = os.environ.get(
        "GEMINI_API_KEY",
        ""
    ).strip()

    print("=" * 65)
    print("          SDG 4 - AI LEARNING TUTOR")
    print("=" * 65)

    print(
        f"Server: http://127.0.0.1:{port}"
    )

    print(
        f"Gemini Model: {GEMINI_MODEL}"
    )

    print(
        "Gemini API Key: "
        + (
            "YES"
            if api_key
            else "NO"
        )
    )

    print("=" * 65)

    app.run(
        host="127.0.0.1",
        port=port,
        debug=True
    )