"""
==========================================================
Prompt Engine
AI Website Generator
==========================================================
"""


def build_prompt(user_prompt: str) -> str:
    """
    Build a complete prompt for Gemini.
    """

    return f"""
You are an expert frontend developer.

Create a complete modern responsive website.

USER REQUEST:
{user_prompt}

RULES:
- Return only HTML.
- Return ONE complete HTML file only.
- Include CSS and JavaScript.
- Responsive layout.
- Modern UI design.
- Beautiful color combination.
- Add animations if suitable.
"""