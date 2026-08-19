from flask import Blueprint, abort, render_template

from app.db import get_db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    db = get_db()
    subjects = db.execute("SELECT * FROM subjects ORDER BY id").fetchall()
    counts = {
        row["subject_id"]: row["n"]
        for row in db.execute("SELECT subject_id, COUNT(*) AS n FROM questions GROUP BY subject_id")
    }
    return render_template("index.html", subjects=subjects, counts=counts)


@bp.route("/quiz/<slug>")
def quiz(slug):
    db = get_db()
    subject = db.execute("SELECT * FROM subjects WHERE slug = ?", (slug,)).fetchone()
    if subject is None:
        abort(404)
    return render_template("quiz.html", subject=subject)
