
import html

from flask import (Flask, render_template, request, Response, session, redirect, url_for,)
import os
import time
from app.core.config import *
from app.database.database import init_db
from app.services.website_generator import generate_website
from app.helpers.validators import validate_prompt
from app.services.history_service import (record_prompt, load_history, remove_history, remove_all_history, statistics, search, load_generated_html,)
from app.services.export_service import (download_html, download_zip,)

# =========================
# FLASK APP
# =========================

app = Flask(__name__)

print("=" * 60)
print(f"{APP_NAME} v{APP_VERSION}")
print(f"Gemini Model : {GEMINI_MODEL}")
print("=" * 60)

app.secret_key = SECRET_KEY

# Initialize database
init_db()


# ==========================================================
# ROUTES
# ==========================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    try:

        prompt = validate_prompt(
            request.form.get("prompt", "")
        )

    except ValueError as e:

        return render_template(
            "index.html",
            error=str(e)
        )

    # ==========================
    # Start Timer
    # ==========================

    start = time.perf_counter()

    # ==========================
    # Generate Website
    # ==========================

    try:

        generated_code = generate_website(prompt)

    except Exception as e:

        return render_template(
        "index.html",
        error=str(e)
        )

    # ==========================
    # Calculate Duration
    # ==========================

    duration = round(
        time.perf_counter() - start,
        2
    )

    # ==========================
    # HTML Size
    # ==========================

    html_size = len(
        generated_code.encode("utf-8")
    )

    # ==========================
    # Save History
    # ==========================

    history_id = record_prompt(

        prompt=prompt,

        status="SUCCESS",

        duration=duration,

        html_size=html_size,

        generated_html=generated_code,
        
    )

    # ==========================
    # Save Session
    # ==========================

    session["last_history_id"] = history_id

    session["last_prompt"] = prompt

    # ==========================
    # Show Result
    # ==========================

    return render_template(

        "result.html",

        prompt=prompt

    )

@app.route("/preview")
def preview():

    history_id = session.get("last_history_id")

    html = load_generated_html(history_id)

    return Response(
        html or "",
        mimetype="text/html"
    )


@app.route("/download")
def download():

    history_id = session.get("last_history_id")
    html = load_generated_html(history_id)
    return download_html(html or "")

@app.route("/download-zip")
def download_zip_file():
    
    history_id = session.get("last_history_id")
    html = load_generated_html(history_id)
    return download_zip(html or "")


@app.route("/get-code")
def get_code():
    history_id = session.get("last_history_id")

    if not history_id:
        return Response("", mimetype="text/html")

    html = load_generated_html(history_id)

    return Response(
        html or "",
        mimetype="text/html"
)



@app.route("/history")
def history():

    history_data = load_history()

    stats = statistics()

    return render_template(
        "history.html",
        history=history_data,
        stats=stats
    )

@app.route("/history/search")
def search_history():

    keyword = request.args.get("q", "").strip()

    history_data = search(keyword)

    stats = statistics()

    return render_template(
        "history.html",
        history=history_data,
        stats=stats
    )

@app.route("/history/delete/<int:history_id>")
def delete_history_route(history_id):

    remove_history(history_id)

    return redirect(url_for("history"))

@app.route("/history/clear")
def clear_history_route():

    remove_all_history()

    return redirect(url_for("history"))

# ==========================================================
# RUN APP
# ==========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )