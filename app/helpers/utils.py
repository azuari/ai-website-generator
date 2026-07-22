"""
==========================================================
Utility Functions
AI Website Generator
==========================================================
"""

import re


def clean_html_response(text):
    """
    Remove markdown code block from Gemini response.
    """

    if not text:
        return ""

    text = re.sub(r"^```html", "", text.strip())
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    return text.strip()


def ensure_html_document(code):
    """
    Make sure response is a complete HTML document.
    """

    if "<html" in code.lower():
        return code

    return f"""<!DOCTYPE html>
<html>
<head>
<title>Generated Website</title>
</head>
<body>

{code}

</body>
</html>
"""