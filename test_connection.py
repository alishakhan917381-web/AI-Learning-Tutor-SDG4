import os
from dotenv import load_dotenv

# Force load from .env
load_dotenv(override=True)

def test_connection():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()

    if not api_key:
        print("STATUS: NO_KEY")
        print("REASON: GEMINI_API_KEY is empty in .env.")
        return False

    if api_key == "your_gemini_api_key_here":
        print("STATUS: PLACEHOLDER_KEY")
        print("REASON: GEMINI_API_KEY is still set to placeholder in .env.")
        return False

    print(f"INFO: Testing Gemini API connection using model '{model_name}'...")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents="Say 'Connected to CampusBot successfully' in 5 words or less.",
        )
        if response and response.text:
            print("STATUS: SUCCESS")
            print(f"RESPONSE: {response.text.strip()}")
            return True
        else:
            print("STATUS: EMPTY_RESPONSE")
            return False
    except Exception as e:
        error_str = str(e)
        print("STATUS: ERROR")
        print(f"ERROR_MESSAGE: {error_str}")
        return False

if __name__ == "__main__":
    test_connection()
