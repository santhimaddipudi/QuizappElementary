# 5th Grade Quiz Zone

An interactive quiz app for 5th grade students, aligned to the Texas Essential
Knowledge and Skills (TEKS) for **Math**, **Science**, and **English (ELAR)**.
Questions live in a SQLite database, so you can add, edit, or remove content
at any time through the built-in admin pages — no code changes required.

## Features

- Home page with a subject picker (Math / Science / English) and live question counts
- One-question-at-a-time quiz flow with instant feedback and an explanation for each answer;
  students must pick an answer before they can move to the next question
- Questions can include an image (diagram, chart, photo, etc.) that shows above the answer
  choices and again in the results review
- Score summary at the end of each quiz, with a full review of every question
- Admin pages are login-protected — kids can browse and take quizzes freely, but everything under
  `/admin` requires the admin username/password (see **Admin login** below)
- `/admin/questions` — add, edit, filter, and delete questions from the browser
- `/admin/import` — bulk-import questions from a `.docx` or `.pdf` document, with a preview step
  before anything is saved, plus bulk delete by subject/topic (with an automatic backup first)
- No-repeat quiz tracking — a student won't see the same question twice until they've worked
  through the whole subject's pool once (tracked per browser, no login needed)
- Every quiz attempt is logged (`quiz_attempts` table) so you can track progress over time
- Question bank of ~960 questions (~320 per subject) covering the major TEKS strands for grade 5,
  skewed toward medium and tricky difficulty, including a mix of diagram/chart questions and 12
  original short reading passages with comprehension questions

## Tech stack

- Python + Flask
- SQLite (file-based database, `instance/quiz.db`)
- Vanilla HTML/CSS/JS front end (no build step required)

## Getting started

```bash
# from the project folder
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```

Then open **http://127.0.0.1:5000** in a browser.

The database is created and seeded automatically the first time you run the
app (look for `instance/quiz.db`). No extra setup step is required.

## Admin login

Everything under `/admin` (managing questions, bulk import, bulk delete) requires logging in.
Default credentials are printed to the console every time you start the app with `python run.py`:

```
Admin login -> username: admin  password: quiz2026
```

**Change these** before letting anyone else use the app, by setting environment variables before
you start it:

```bash
# Windows (PowerShell)
$env:ADMIN_USERNAME = "yourname"
$env:ADMIN_PASSWORD = "a-stronger-password"
python run.py

# macOS/Linux
ADMIN_USERNAME=yourname ADMIN_PASSWORD=a-stronger-password python run.py
```

Kids using the quiz pages never see or need these credentials — only `/admin/*` is gated. This is
a simple username/password check meant for trusted local/home use, not hardened for a public
deployment.

## Managing questions

Go to **Manage Questions** in the nav bar (`/admin/questions`) to:

- Filter questions by subject
- Add a new question (pick subject, topic/TEKS strand, 4 choices, correct
  answer, an explanation, and a difficulty level)
- Edit or delete any existing question
- Optionally attach an image to a question — upload a PNG/JPG/GIF/WEBP/SVG right from the
  form and it's saved automatically and shown in the quiz. (Advanced: you can instead type
  the path to a file you've already placed under `app/static/`, e.g. `img/diagrams/foo.svg`.)

Changes are saved straight to the database and show up in quizzes immediately.

## Bulk-importing questions from a document

Go to **Import from Document** (`/admin/import`) and upload a `.docx` or `.pdf`
file. Each question must follow this format, with a blank line between
questions:

```
Q: What is 5 + 3?
A) 6
B) 7
C) 8
D) 9
Answer: C
Explanation: 5 + 3 = 8.
```

- `Explanation:`, `Topic:`, and `Difficulty:` lines are optional.
- `Topic:` must exactly match one of the subject's existing topic names, or the
  question falls back to whatever default topic you chose on the upload form.
- `Difficulty:` must be `easy`, `medium`, or `hard` (defaults to `medium`).
- Only **text-based** PDFs work — a scanned/photographed PDF has no
  extractable text and will be rejected with an explanation.
- **Images in `.docx` files:** a picture placed directly above or inside a question is
  automatically detected and attached to that question — no special formatting needed.
  This only works for `.docx` (not `.pdf`); add an image afterwards from the question's
  Edit page if you imported from a PDF.

Nothing is written to the database until you review a **preview** (showing
every parsed question — including a thumbnail of any detected image — plus a list of
anything that failed to parse and why) and click **Confirm Import**.

Two ready-made examples (one question about math, one about science, using
every optional field) are in [`samples/sample_questions.docx`](samples/sample_questions.docx)
and [`samples/sample_questions.pdf`](samples/sample_questions.pdf) — open either one as a
starting template.

## Bulk deleting questions

On `/admin/questions`, open **Bulk delete questions by subject/topic**, choose
a subject (and optionally narrow it to one topic), and you'll land on a
confirmation page showing exactly how many questions will be deleted. Typing
`DELETE` is required to proceed. A full backup of `instance/quiz.db` is saved
to `instance/backups/` automatically before the delete runs, in case you need
to restore it (just copy the backup file back over `instance/quiz.db`).

### Resetting or reseeding the database from the command line

```bash
# Wipe all tables and reload just the starter questions
flask --app run init-db

# Wipe all tables without reseeding (empty database)
flask --app run init-db --no-seed

# Add the starter questions again without wiping existing data
# (skip this if you've already customized your question bank —
# it will add duplicate starter questions)
flask --app run seed-db
```

## Project structure

```
app/
  __init__.py       Flask app factory
  db.py             SQLite connection + CLI commands
  schema.sql        Database schema (subjects, topics, questions, quiz_attempts)
  seed_data.py      Starter TEKS-aligned question bank + wires in the generators below
  generators/       Scripts that generate the ~300-question-per-subject bank (math/science/english)
  importers.py      Parses uploaded .docx/.pdf documents into question records
  routes_main.py    Home page + quiz page routes
  routes_api.py     JSON API used by the quiz page (fetch questions, submit answers)
  routes_admin.py   Question management: list/add/edit/delete, bulk import, bulk delete
  templates/        Jinja2 HTML templates
  static/           CSS and JS
run.py              App entry point
```

## Notes on TEKS alignment

Topics are labeled with the relevant TEKS strand (e.g. "Number & Operations —
TEKS 5.3") to help you organize content by standard. These are strand-level
references for organizing questions, not verbatim standard text. Always check
the official TEKS documents at [tea.texas.gov](https://tea.texas.gov) when
using this for formal instruction or assessment.

## Next steps you might want

- Harden admin auth (hashed passwords, rate limiting) before deploying anywhere
  public — the current username/password check is meant for trusted local/home use
- Add a "review by topic" mode to focus practice on one TEKS strand at a time
