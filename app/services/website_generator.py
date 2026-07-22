"""
==========================================================
Website Generator Service
==========================================================
"""

from app.prompt_engine import build_prompt
from app.services.gemini_service import generate_with_gemini
from app.helpers.utils import (
    clean_html_response,
    ensure_html_document,
)
from app.helpers.error_pages import (
    no_response_page,
    generation_error_page,
)


def generate_website(prompt: str) -> str:
    """
    Generate a complete website using Gemini.
    """

    try:

        prompt_text = build_prompt(prompt)

        response = generate_with_gemini(prompt_text)

        if not response.text:
            return no_response_page()

        html = clean_html_response(response.text)

        html = ensure_html_document(html)

        return html

    except Exception as e:

        return generation_error_page(str(e))