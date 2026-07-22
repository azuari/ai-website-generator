"""
==========================================================
AI Website Generator Configuration
Version : 1.0 RC2
==========================================================
"""

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "AI Website Generator"
APP_VERSION = "1.0 RC2"

# ==========================================================
# FLASK
# ==========================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is missing."
    )

# ==========================================================
# GEMINI
# ==========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"

FALLBACK_MODELS = [
    "gemini-flash-latest",
    "gemini-2.5-flash-lite"
]

# ==========================================================
# RETRY
# ==========================================================

MAX_RETRY = 3

RETRY_DELAY = 2

# ==========================================================
# DATABASE
# ==========================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_NAME = BASE_DIR / "history.db"