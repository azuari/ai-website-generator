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

    class DummyResponse:
        text = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dummy Test</title>

    <style>
        body{
            font-family: Arial, sans-serif;
            text-align:center;
            margin-top:100px;
            background:#f5f5f5;
        }

        h1{
            color:#0d6efd;
        }
    </style>
</head>

<body>

<h1>AI Website Generator</h1>

<h2>Dummy Response Berjaya!</h2>

<p>Flask ✔</p>
<p>Render ✔</p>
<p>Database ✔</p>

</body>
</html>
"""

    return DummyResponse()