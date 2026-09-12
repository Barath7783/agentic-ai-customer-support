import time

from google import genai
from google.genai.errors import ServerError

from config import GEMINI_API_KEY, MODEL_NAME


def get_client():
    if not GEMINI_API_KEY:
        return None

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_response(system_prompt: str, user_prompt: str) -> str:
    client = get_client()

    if client is None:
        return (
            "Demo mode: GEMINI_API_KEY is not configured. "
            "The support-agent workflow is working, "
            "but the AI model is not connected yet."
        )

    prompt = f"""
SYSTEM:
{system_prompt}

USER:
{user_prompt}
"""

    # Retry Gemini temporarily unavailable errors
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            return response.text

        except ServerError:
            if attempt == 2:
                return (
                    "The AI service is temporarily busy. "
                    "Please try again in a few seconds."
                )

            # 2 seconds, then 4 seconds
            time.sleep(2 ** (attempt + 1))

    return "Unable to generate a response right now."
