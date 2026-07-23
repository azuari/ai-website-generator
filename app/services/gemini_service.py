"""
==========================================================
Gemini AI Service
AI Website Generator v1.0 RC2
==========================================================
"""

import time

from google import genai
from google.genai.errors import ClientError

from app.core.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    FALLBACK_MODELS,
    MAX_RETRY,
    RETRY_DELAY,
)

# ==========================================================
# GEMINI CLIENT
# ==========================================================

client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================================================
# GENERATE WITH GEMINI
# ==========================================================

def generate_with_gemini(prompt):

    models = [GEMINI_MODEL] + FALLBACK_MODELS

    last_error = None

    for model in models:

        print("=" * 60)
        print(f"Trying model : {model}")
        print("=" * 60)

        for attempt in range(MAX_RETRY):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if (
                    response
                    and hasattr(response, "text")
                    and response.text
                ):

                    print(f"SUCCESS : {model}")

                    return response

                print("Empty response received.")

                break

            except ClientError as e:

                last_error = e

                error = str(e)

                print(error)

                # 503 = Busy
                if "503" in error or "UNAVAILABLE" in error:

                    print(
                        f"{model} busy..."
                        f" retry {attempt+1}/{MAX_RETRY}"
                    )

                    time.sleep(RETRY_DELAY)

                    continue

                # 429 = Quota
                if "429" in error:

                    print("Quota exceeded.")

                    break

                # other client error

                break

            except Exception as e:

                last_error = e

                print(f"Unexpected Error : {e}")

                break

    raise RuntimeError(
        "Gemini AI sedang sibuk. "
        "Sila cuba semula dalam beberapa minit."
    ) from last_error