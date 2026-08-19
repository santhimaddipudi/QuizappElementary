import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from app.db import get_db
from app.importers import ImportError_, extract_text, parse_questions_text

bp = Blueprint("admin", __name__, url_prefix="/admin")

MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


@bp.before_request
def require_admin_login():
    if request.endpoint == "admin.login":
        return None
    if not session.get("is_admin"):
        return redirect(url_for("admin.login", next=request.path))
    return None


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == current_app.config["ADMIN_USERNAME"] and password == current_app.config["ADMIN_PASSWORD"]:
            session.clear()
            session["is_admin"] = True
            session.permanent = True
            next_url = request.args.get("next")
            if not next_url or not next_url.startswith("/admin"):
                next_url = url_for("admin.list_questions")
            return redirect(next_url)
        error = "Incorrect username or password."
    return render_template("admin/login.html", error=error)


@bp.route("/logout", methods=["POST"])
def logout():
    session.pop("is_admin", None)
    flash("Logged out.", "success")
    return redirect(url_for("main.index"))


def _import_tmp_dir():
    path = Path(current_app.instance_path) / "import_tmp"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _backup_database():
    """Copy the live database before a destructive bulk action, so a mistake
    can be undone by restoring the newest file in instance/backups/."""
    db_path = Path(current_app.config["DATABASE"])
    backups_dir = Path(current_app.instance_path) / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backups_dir / f"quiz_backup_{timestamp}.db"
    if db_path.exists():
        shutil.copy2(db_path, backup_path)
    return backup_path


@bp.route("/")
def dashboard():
    return redirect(url_for("admin.list_questions"))


@bp.route("/questions")
def list_questions():
    db = get_db()
    subject_slug = request.args.get("subject", "")
    subjects = db.execute("SELECT * FROM subjects ORDER BY id").fetchall()

    query = """SELECT q.*, s.name AS subject_name, s.slug AS subject_slug, t.name AS topic_name
               FROM questions q
               JOIN subjects s ON s.id = q.subject_id
               LEFT JOIN topics t ON t.id = q.topic_id"""
    params = []
    if subject_slug:
        query += " WHERE s.slug = ?"
        params.append(subject_slug)
    query += " ORDER BY s.id, t.id, q.id"

    questions = db.execute(query, params).fetchall()
    topics_by_subject = {s["id"]: _topics_for_subject(db, s["id"]) for s in subjects}
    return render_template(
        "admin/list.html", questions=questions, subjects=subjects, selected_subject=subject_slug,
        topics_by_subject=topics_by_subject,
    )


def _topics_for_subject(db, subject_id):
    return db.execute(
        "SELECT * FROM topics WHERE subject_id = ? ORDER BY id", (subject_id,)
    ).fetchall()


@bp.route("/questions/new", methods=["GET", "POST"])
def new_question():
    db = get_db()
    subjects = db.execute("SELECT * FROM subjects ORDER BY id").fetchall()

    if request.method == "POST":
        form = request.form
        db.execute(
            """INSERT INTO questions
               (subject_id, topic_id, question_text, choice_a, choice_b, choice_c, choice_d,
                correct_choice, explanation, difficulty, image_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                form["subject_id"],
                form.get("topic_id") or None,
                form["question_text"].strip(),
                form["choice_a"].strip(),
                form["choice_b"].strip(),
                form["choice_c"].strip(),
                form["choice_d"].strip(),
                form["correct_choice"],
                form.get("explanation", "").strip(),
                form.get("difficulty", "medium"),
                form.get("image_path", "").strip() or None,
            ),
        )
        db.commit()
        flash("Question added.", "success")
        return redirect(url_for("admin.list_questions"))

    topics_by_subject = {s["id"]: _topics_for_subject(db, s["id"]) for s in subjects}
    return render_template(
        "admin/form.html", question=None, subjects=subjects, topics_by_subject=topics_by_subject
    )


@bp.route("/questions/<int:question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    db = get_db()
    subjects = db.execute("SELECT * FROM subjects ORDER BY id").fetchall()

    if request.method == "POST":
        form = request.form
        db.execute(
            """UPDATE questions SET
                   subject_id = ?, topic_id = ?, question_text = ?, choice_a = ?, choice_b = ?,
                   choice_c = ?, choice_d = ?, correct_choice = ?, explanation = ?, difficulty = ?,
                   image_path = ?
               WHERE id = ?""",
            (
                form["subject_id"],
                form.get("topic_id") or None,
                form["question_text"].strip(),
                form["choice_a"].strip(),
                form["choice_b"].strip(),
                form["choice_c"].strip(),
                form["choice_d"].strip(),
                form["correct_choice"],
                form.get("explanation", "").strip(),
                form.get("difficulty", "medium"),
                form.get("image_path", "").strip() or None,
                question_id,
            ),
        )
        db.commit()
        flash("Question updated.", "success")
        return redirect(url_for("admin.list_questions"))

    question = db.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    if question is None:
        flash("Question not found.", "error")
        return redirect(url_for("admin.list_questions"))

    topics_by_subject = {s["id"]: _topics_for_subject(db, s["id"]) for s in subjects}
    return render_template(
        "admin/form.html", question=question, subjects=subjects, topics_by_subject=topics_by_subject
    )


@bp.route("/questions/<int:question_id>/delete", methods=["POST"])
def delete_question(question_id):
    db = get_db()
    db.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    db.commit()
    flash("Question deleted.", "success")
    return redirect(url_for("admin.list_questions"))


# ------------------------------------------------------------------ Bulk import

@bp.route("/import", methods=["GET"])
def import_form():
    db = get_db()
    subjects = db.execute("SELECT * FROM subjects ORDER BY id").fetchall()
    topics_by_subject = {s["id"]: _topics_for_subject(db, s["id"]) for s in subjects}
    return render_template("admin/import.html", subjects=subjects, topics_by_subject=topics_by_subject)


@bp.route("/import/preview", methods=["POST"])
def import_preview():
    db = get_db()
    subjects = db.execute("SELECT * FROM subjects ORDER BY id").fetchall()
    topics_by_subject = {s["id"]: _topics_for_subject(db, s["id"]) for s in subjects}

    subject_id = request.form.get("subject_id")
    default_topic_id = request.form.get("default_topic_id") or None
    uploaded = request.files.get("document")

    if not subject_id:
        flash("Please choose a subject.", "error")
        return redirect(url_for("admin.import_form"))
    if not uploaded or not uploaded.filename:
        flash("Please choose a .docx or .pdf file to upload.", "error")
        return redirect(url_for("admin.import_form"))

    file_bytes = uploaded.read()
    if len(file_bytes) > MAX_UPLOAD_BYTES:
        flash("That file is too large (max 5 MB). Try splitting it into smaller uploads.", "error")
        return redirect(url_for("admin.import_form"))

    try:
        text = extract_text(uploaded.filename, file_bytes)
        questions, errors = parse_questions_text(text)
    except ImportError_ as exc:
        flash(str(exc), "error")
        return redirect(url_for("admin.import_form"))

    subject = db.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
    topics = _topics_for_subject(db, subject_id)
    topic_by_name = {t["name"].strip().lower(): t["id"] for t in topics}

    for q in questions:
        override = q.pop("topic_override", None)
        matched_topic_id = topic_by_name.get(override.strip().lower()) if override else None
        q["topic_id"] = matched_topic_id or (int(default_topic_id) if default_topic_id else None)
        q["topic_name"] = next((t["name"] for t in topics if t["id"] == q["topic_id"]), None)

    token = uuid.uuid4().hex
    payload = {"subject_id": int(subject_id), "questions": questions}
    tmp_path = _import_tmp_dir() / f"{token}.json"
    tmp_path.write_text(json.dumps(payload), encoding="utf-8")

    return render_template(
        "admin/import_preview.html",
        subject=subject,
        questions=questions,
        errors=errors,
        token=token,
        filename=uploaded.filename,
    )


@bp.route("/import/confirm", methods=["POST"])
def import_confirm():
    token = request.form.get("token", "")
    tmp_path = _import_tmp_dir() / f"{token}.json"
    if not token or not tmp_path.exists():
        flash("This import has expired — please upload the file again.", "error")
        return redirect(url_for("admin.import_form"))

    payload = json.loads(tmp_path.read_text(encoding="utf-8"))
    subject_id = payload["subject_id"]
    questions = payload["questions"]

    db = get_db()
    for q in questions:
        db.execute(
            """INSERT INTO questions
               (subject_id, topic_id, question_text, choice_a, choice_b, choice_c, choice_d,
                correct_choice, explanation, difficulty, image_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
            (
                subject_id, q.get("topic_id"), q["question_text"], q["choice_a"], q["choice_b"],
                q["choice_c"], q["choice_d"], q["correct_choice"], q["explanation"], q["difficulty"],
            ),
        )
    db.commit()
    tmp_path.unlink(missing_ok=True)

    flash(f"Imported {len(questions)} question(s) successfully.", "success")
    return redirect(url_for("admin.list_questions"))


@bp.route("/import/cancel", methods=["POST"])
def import_cancel():
    token = request.form.get("token", "")
    tmp_path = _import_tmp_dir() / f"{token}.json"
    tmp_path.unlink(missing_ok=True)
    flash("Import cancelled — nothing was added.", "success")
    return redirect(url_for("admin.import_form"))


# ------------------------------------------------------------------ Bulk delete

@bp.route("/questions/bulk-delete-preview", methods=["POST"])
def bulk_delete_preview():
    db = get_db()
    subject_id = request.form.get("subject_id")
    topic_id = request.form.get("topic_id") or None

    if not subject_id:
        flash("Please choose a subject to bulk delete from.", "error")
        return redirect(url_for("admin.list_questions"))

    query = "SELECT COUNT(*) AS n FROM questions WHERE subject_id = ?"
    params = [subject_id]
    if topic_id:
        query += " AND topic_id = ?"
        params.append(topic_id)
    count = db.execute(query, params).fetchone()["n"]

    subject = db.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
    topic = db.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone() if topic_id else None

    return render_template(
        "admin/bulk_delete_confirm.html", subject=subject, topic=topic, count=count, topic_id=topic_id or ""
    )


@bp.route("/questions/bulk-delete", methods=["POST"])
def bulk_delete_confirm():
    subject_id = request.form.get("subject_id")
    topic_id = request.form.get("topic_id") or None
    confirm_text = request.form.get("confirm_text", "")

    if confirm_text.strip() != "DELETE":
        flash("Bulk delete cancelled — you must type DELETE exactly to confirm.", "error")
        return redirect(url_for("admin.list_questions"))

    _backup_database()

    db = get_db()
    query = "DELETE FROM questions WHERE subject_id = ?"
    params = [subject_id]
    if topic_id:
        query += " AND topic_id = ?"
        params.append(topic_id)
    cur = db.execute(query, params)
    db.commit()

    flash(f"Bulk deleted {cur.rowcount} question(s). A backup of the database was saved first.", "success")
    return redirect(url_for("admin.list_questions"))
