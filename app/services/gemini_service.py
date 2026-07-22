"""
==========================================================
Gemini AI Service
AI Website Generator v1.0 RC2
==========================================================
"""

import time
from urllib import response
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
    """
    Generate content using Gemini with
    retry and fallback models.
    """

    models = [GEMINI_MODEL] + FALLBACK_MODELS

    last_error = None

    for model in models:

        print(f"\nTrying model: {model}")

        for attempt in range(MAX_RETRY):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                print("=" * 60)
                print(response)
                print("=" * 60)
                
                print(f"SUCCESS using {model}")

                return response

            except ClientError as e:

                last_error = e
                error_text = str(e)

                # 503 - Model Busy
                if "503" in error_text or "UNAVAILABLE" in error_text:

                    print(
                        f"{model} busy "
                        f"(Attempt {attempt+1}/{MAX_RETRY})"
                    )

                    time.sleep(RETRY_DELAY)
                    continue

                # 429 - Quota
                elif "429" in error_text:

                    print(f"Quota exceeded for {model}")
                    break

                else:

                    print(error_text)
                    break

            except Exception as e:

                last_error = e
                print(e)
                break

    raise last_error