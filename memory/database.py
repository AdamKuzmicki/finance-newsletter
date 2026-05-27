"""
Database Module
---------------
Manages SQLite database for tracking your learning progress.

Why SQLite?
- It's a file-based database (just one .db file)
- Built into Python - no installation needed
- Perfect for single-user apps like this
- You can open the .db file with DB Browser for SQLite to inspect it visually

Key concept: This is your agent's "long-term memory" - it remembers what
you've already learned so it doesn't repeat lessons and can build on prior topics.
"""

import sqlite3
import os
from datetime import date
from config.settings import TOPICS_IN_ORDER

# Database file location
DB_PATH = "memory/newsletter.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Create the database and tables if they don't exist.
    Called once on startup.
    """
    # Create memory directory if needed
    os.makedirs("memory", exist_ok=True)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Read and execute our schema SQL file
    with open("memory/schema.sql", "r") as f:
        schema = f.read()
    
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("✓ Database initialized")


def get_next_topic() -> dict:
    """
    Determine what finance topic to teach today.
    
    Logic:
    1. Look up which topic index we're at
    2. If a topic hasn't been covered recently, return it
    3. Advance to the next topic after covering it
    
    Returns a dict with topic name, lesson number, and difficulty level.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get current position in curriculum
    cursor.execute(
        "SELECT value FROM user_profile WHERE key = 'current_topic_index'"
    )
    row = cursor.fetchone()
    topic_index = int(row[0]) if row else 0
    
    # Wrap around if we've completed all topics (start over at higher difficulty)
    if topic_index >= len(TOPICS_IN_ORDER):
        topic_index = 0
        # Increase difficulty for the second pass
        cursor.execute(
            "UPDATE user_profile SET value = '0' WHERE key = 'current_topic_index'"
        )
    
    topic_name = TOPICS_IN_ORDER[topic_index]
    
    # Check if this topic has been covered before
    cursor.execute(
        "SELECT lesson_number, difficulty_level FROM learning_progress WHERE topic = ?",
        (topic_name,),
    )
    existing = cursor.fetchone()
    
    if existing:
        lesson_number = existing[0] + 1
        difficulty_level = existing[1]
    else:
        lesson_number = 1
        difficulty_level = 1
    
    conn.close()
    
    return {
        "topic": topic_name,
        "lesson_number": lesson_number,
        "difficulty_level": difficulty_level,
        "topic_index": topic_index,
    }


def record_lesson_taught(topic: str, topic_index: int):
    """
    After a newsletter is sent, record that we taught this topic today.
    Advance to the next topic for tomorrow.
    """
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    # Upsert learning progress
    cursor.execute("""
        INSERT INTO learning_progress (topic, lesson_number, last_taught, difficulty_level)
        VALUES (?, 1, ?, 1)
        ON CONFLICT(topic) DO UPDATE SET
            lesson_number = lesson_number + 1,
            last_taught = excluded.last_taught
    """, (topic, today))
    
    # Record newsletter history
    cursor.execute("""
        INSERT INTO newsletter_history (date, topic_covered)
        VALUES (?, ?)
    """, (today, topic))
    
    # Advance to next topic
    next_index = topic_index + 1
    cursor.execute(
        "UPDATE user_profile SET value = ? WHERE key = 'current_topic_index'",
        (str(next_index),)
    )
    
    # Increment newsletters sent counter
    cursor.execute("""
        UPDATE user_profile
        SET value = CAST(CAST(value AS INTEGER) + 1 AS TEXT)
        WHERE key = 'newsletters_sent'
    """)
    
    conn.commit()
    conn.close()


def get_recent_topics(n: int = 5) -> list[str]:
    """Return the last N topics covered, for context in prompts."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT topic_covered FROM newsletter_history
        ORDER BY date DESC LIMIT ?
    """, (n,))
    
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows if r[0]]


def get_newsletters_sent() -> int:
    """Return total number of newsletters sent."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT value FROM user_profile WHERE key = 'newsletters_sent'"
    )
    row = cursor.fetchone()
    conn.close()
    return int(row[0]) if row else 0
