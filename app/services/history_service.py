"""
==========================================================
History Service
==========================================================
"""

from app.database.database import (save_history, load_history as db_load_history, delete_history, clear_history, get_statistics, search_history, get_generated_html)

from app.core.config import GEMINI_MODEL

def record_prompt(prompt, status, duration, html_size, generated_html):

    history_id = save_history(
        prompt=prompt, 
        model=GEMINI_MODEL, 
        status=status, 
        duration=duration, 
        html_size=html_size, 
        generated_html=generated_html,
    )

    return history_id

def load_history():

    return db_load_history()

# =========================
# SEARCH HISTORY
# =========================

def search(keyword):
    """
    Search prompt history.
    """
    return search_history(keyword)


def remove_history(history_id):

    delete_history(history_id)


def remove_all_history():

    clear_history()

def statistics():

    return get_statistics()

# =========================
# GET GENERATED HTML
# =========================

def load_generated_html(history_id):

    return get_generated_html(history_id)