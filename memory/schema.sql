-- This SQL file defines the tables for your learning database.
-- SQLite will execute this to create the database structure.

CREATE TABLE IF NOT EXISTS learning_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,                    -- lesson topic name
    lesson_number INTEGER DEFAULT 0,        -- how many times covered
    difficulty_level INTEGER DEFAULT 1,     -- 1=beginner, 2=intermediate, 3=advanced
    last_taught DATE,                       -- when last covered
    comprehension_score REAL DEFAULT 0.5,   -- 0.0 to 1.0 (future: from quizzes)
    notes TEXT                              -- any notes about this topic
);

CREATE TABLE IF NOT EXISTS newsletter_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    topic_covered TEXT,                     -- which finance topic was taught
    market_summary TEXT,                    -- brief market summary (for context)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_profile (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- Default user profile
INSERT OR IGNORE INTO user_profile VALUES ('name', 'Student');
INSERT OR IGNORE INTO user_profile VALUES ('start_date', date('now'));
INSERT OR IGNORE INTO user_profile VALUES ('current_topic_index', '0');
INSERT OR IGNORE INTO user_profile VALUES ('newsletters_sent', '0');
