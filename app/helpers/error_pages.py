"""
==========================================================
Error Pages
AI Website Generator
==========================================================
"""

from app.core.constants import (
    ERROR_TITLE,
    NO_RESPONSE_HTML_TITLE
)


def no_response_page():
    """
    HTML shown when Gemini returns no response.
    """

    return f"""
<!DOCTYPE html>
<html>
<head>

<title>{NO_RESPONSE_HTML_TITLE}</title>

<style>

body{{
    background:#111827;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}}

.box{{
    background:#1f2937;
    padding:30px;
    border-radius:16px;
}}

</style>

</head>

<body>

<div class="box">

<h1>No response from Gemini</h1>

</div>

</body>

</html>
"""


def generation_error_page(message):
    """
    HTML shown when generation fails.
    """

    return f"""
<!DOCTYPE html>
<html>

<head>

<title>{ERROR_TITLE}</title>

<style>

body{{
    margin:0;
    padding:40px;
    background:#111827;
    color:white;
    font-family:Arial;
}}

.error-box{{
    background:#1f2937;
    padding:30px;
    border-radius:18px;
}}

h1{{
    color:#ef4444;
}}

pre{{
    background:#0f172a;
    padding:15px;
    border-radius:10px;
    overflow:auto;
}}

</style>

</head>

<body>

<div class="error-box">

<h1>Generation Error</h1>

<pre>{message}</pre>

</div>

</body>

</html>
"""