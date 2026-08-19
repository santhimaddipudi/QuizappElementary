import random

from flask import Blueprint, jsonify, request

from app.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")

DEFAULT_QUESTION_COUNT = 10


@bp.route("/subjects")
def subjects():
    db = get_db()
    rows = db.execute("SELECT * FROM subjects ORDER BY id").fetchall()
    return jsonify([dict(r) for r in rows])


@bp.route("/quiz/<slug>")
def quiz_questions(slug):
    db = get_db()
    subject = db.execute("SELECT * FROM subjects WHERE slug = ?", (slug,)).fetchone()
    if subject is None:
        return jsonify({"error": "Unknown subject"}), 404

    count = request.args.get("count", DEFAULT_QUESTION_COUNT, type=int)
    exclude_param = request.args.get("exclude", "")
    exclude_ids = {int(p) for p in exclude_param.split(",") if p.strip().isdigit()}

    rows = db.execute(
        """SELECT q.id, q.question_text, q.choice_a, q.choice_b, q.choice_c, q.choice_d,
                  q.difficulty, q.image_path, t.name AS topic
           FROM questions q
           LEFT JOIN topics t ON t.id = q.topic_id
           WHERE q.subject_id = ?""",
        (subject["id"],),
    ).fetchall()

    all_questions = [dict(r) for r in rows]
    random.shuffle(all_questions)

    unseen = [q for q in all_questions if q["id"] not in exclude_ids]
    cycle_reset = False
    if len(unseen) >= count:
        selected = unseen[:count]
    else:
        # Not enough never-seen questions left to fill this quiz — use what's left,
        # then top up from the already-seen pool, starting a fresh no-repeat cycle.
        selected = list(unseen)
        seen_pool = [q for q in all_questions if q["id"] in exclude_ids]
        random.shuffle(seen_pool)
        selected += seen_pool[: count - len(selected)]
        cycle_reset = True

    return jsonify(
        {
            "subject": dict(subject),
            "questions": selected,
            "cycle_reset": cycle_reset,
            "total_available": len(all_questions),
        }
    )


@bp.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json(force=True, silent=True) or {}
    subject_slug = data.get("subject")
    student_name = (data.get("student_name") or "").strip() or None
    answers = data.get("answers", [])

    db = get_db()
    subject = db.execute("SELECT * FROM subjects WHERE slug = ?", (subject_slug,)).fetchone()
    if subject is None:
        return jsonify({"error": "Unknown subject"}), 404

    results = []
    score = 0
    for ans in answers:
        qid = ans.get("question_id")
        chosen = ans.get("choice")
        row = db.execute(
            "SELECT id, correct_choice, explanation, question_text FROM questions WHERE id = ?",
            (qid,),
        ).fetchone()
        if row is None:
            continue
        is_correct = chosen == row["correct_choice"]
        if is_correct:
            score += 1
        results.append(
            {
                "question_id": qid,
                "question_text": row["question_text"],
                "chosen": chosen,
                "correct_choice": row["correct_choice"],
                "is_correct": is_correct,
                "explanation": row["explanation"],
            }
        )

    total = len(results)
    db.execute(
        "INSERT INTO quiz_attempts (student_name, subject_id, score, total) VALUES (?, ?, ?, ?)",
        (student_name, subject["id"], score, total),
    )
    db.commit()

    return jsonify({"score": score, "total": total, "results": results})
