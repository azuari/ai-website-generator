"""
==========================================================
Database Module
AI Website Generator
==========================================================
"""

import sqlite3

from app.core.config import DATABASE_NAME

# =========================
# GET CONNECTION
# =========================

def get_connection():
    """
    Create a new database connection.
    """
    return sqlite3.connect(DATABASE_NAME)

# =========================
# DATABASE
# =========================

def init_db():
    """
    Initialize database and create tables if they do not exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute ("""
                  
    CREATE TABLE IF NOT EXISTS history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        prompt TEXT NOT NULL,

        model TEXT,

        status TEXT,

        duration REAL,

        html_size INTEGER,

        generated_html TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    try:

        cursor.execute("""

            ALTER TABLE history

            ADD COLUMN generated_html TEXT

        """)
        
    except sqlite3.OperationalError as e:

        if "duplicate column name" not in str(e):

            raise
        
    conn.commit()
    conn.close()


# =========================
# SAVE HISTORY
# =========================


def save_history(prompt, model, status, duration, html_size, generated_html):
   conn = get_connection() 
   cursor = conn.cursor() 
   cursor.execute( 
       """ 
       INSERT INTO history 
       ( 
            prompt, model, status, duration, html_size, generated_html ) 
            VALUES (?, ?, ?, ?, ?, ?) 
            """, (
                     prompt, model, status, duration, html_size, generated_html
                ) 
    )

   history_id = cursor.lastrowid 
   conn.commit() 
   conn.close()
   return history_id

# =========================
# LOAD HISTORY
# =========================

def load_history(limit=20):
    """
    Return latest prompt history.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute (
    """
    SELECT

                id, prompt, model, status, duration, html_size,

                created_at

                FROM history

                ORDER BY id DESC

                LIMIT ?
            """, (limit,))

    history = cursor.fetchall()

    conn.close()

    return history

# =========================
# DELETE HISTORY
# =========================

def delete_history(history_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE id = ?",
        (history_id,)
    )

    conn.commit()
    conn.close()


# =========================
# CLEAR HISTORY
# =========================

def clear_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")

    conn.commit()
    conn.close()


# =========================
# HISTORY STATISTICS
# =========================

def get_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            COUNT(*),

            ROUND(AVG(duration),2),

            ROUND(AVG(html_size),0),

            MAX(created_at)

        FROM history
        """
    )

    stats = cursor.fetchone()

    conn.close()

    return {
        "total": stats[0] or 0,
        "avg_duration": stats[1] or 0,
        "avg_size": stats[2] or 0,
        "latest": stats[3] or "-"
    }

# =========================
# SEARCH HISTORY
# =========================

def search_history(keyword, limit=20):
    """
    Search history by prompt.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            prompt,
            model,
            status,
            duration,
            html_size,
            created_at
        FROM history
        WHERE prompt LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (f"%{keyword}%", limit)
    )

    history = cursor.fetchall()

    conn.close()

    return history

# =========================
# GET GENERATED HTML
# =========================

def get_generated_html(history_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT generated_html
        FROM history
        WHERE id = ?
        """,
        (history_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None