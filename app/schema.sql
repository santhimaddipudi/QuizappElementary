DROP TABLE IF EXISTS quiz_attempts;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS subjects;

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    color TEXT NOT NULL,
    icon TEXT NOT NULL
);

CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    name TEXT NOT NULL,
    teks_strand TEXT
);

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    topic_id INTEGER REFERENCES topics(id),
    question_text TEXT NOT NULL,
    choice_a TEXT NOT NULL,
    choice_b TEXT NOT NULL,
    choice_c TEXT NOT NULL,
    choice_d TEXT NOT NULL,
    correct_choice TEXT NOT NULL CHECK (correct_choice IN ('A', 'B', 'C', 'D')),
    explanation TEXT,
    difficulty TEXT NOT NULL DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
