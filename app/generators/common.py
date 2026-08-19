"""Shared helpers for the bulk question generators (math_gen, science_gen, english_gen)."""


def make_question(subject, topic, question_text, correct_text, distractors, explanation, difficulty, rng):
    """Build a question dict with choices shuffled into a random A-D position.

    distractors: list of exactly 3 wrong-answer strings, all distinct from correct_text
    and from each other.
    """
    options = [(correct_text, True)] + [(d, False) for d in distractors]

    # Guard against accidental duplicate option text (would break correctness).
    seen = set()
    deduped = []
    for text, is_correct in options:
        if text in seen:
            continue
        seen.add(text)
        deduped.append((text, is_correct))
    if len(deduped) != 4:
        raise ValueError(f"Question has duplicate/insufficient options: {question_text!r} -> {options!r}")

    rng.shuffle(deduped)
    letters = ["A", "B", "C", "D"]
    correct_choice = None
    choice_values = {}
    for letter, (text, is_correct) in zip(letters, deduped):
        choice_values[letter] = text
        if is_correct:
            correct_choice = letter

    return {
        "subject": subject,
        "topic": topic,
        "question_text": question_text,
        "choice_a": choice_values["A"],
        "choice_b": choice_values["B"],
        "choice_c": choice_values["C"],
        "choice_d": choice_values["D"],
        "correct_choice": correct_choice,
        "explanation": explanation,
        "difficulty": difficulty,
        "image_path": None,
    }


def fill_distractors(existing, correct, make_candidate, max_tries=80):
    """Top up a distractor list to 3 unique, non-correct values.

    existing: distractor strings already collected (may already be >= 3).
    make_candidate(try_index) -> a candidate string (or None to skip).
    Bounded by max_tries so a bad candidate function can never hang the generator;
    the caller should skip this question instance if fewer than 3 come back.
    """
    distractors = list(dict.fromkeys(existing))  # dedupe, preserve order
    if correct in distractors:
        distractors.remove(correct)
    tries = 0
    while len(distractors) < 3 and tries < max_tries:
        candidate = make_candidate(tries)
        tries += 1
        if candidate is None:
            continue
        if candidate != correct and candidate not in distractors:
            distractors.append(candidate)
    return distractors[:3]


def _question_identity(q):
    """A question is only a true duplicate if its text AND its full set of
    choices match — the same phrasing with a different correct answer (e.g.
    'Which of these is a solid?' asked about different items) is not a dup."""
    choices = frozenset([q["choice_a"], q["choice_b"], q["choice_c"], q["choice_d"]])
    return (q["question_text"], choices)


def dedupe_pool(pool):
    seen = set()
    result = []
    for q in pool:
        key = _question_identity(q)
        if key in seen:
            continue
        seen.add(key)
        result.append(q)
    return result


def select_balanced(pool, easy_n, medium_n, hard_n, rng):
    """Like select_by_difficulty, but round-robins across topics within each
    difficulty bucket so no single topic dominates the final selection just
    because its templates happened to generate the largest raw pool."""
    pool = dedupe_pool(pool)
    topics = sorted(set(q["topic"] for q in pool))

    result = []
    for level, target in (("easy", easy_n), ("medium", medium_n), ("hard", hard_n)):
        bucket_by_topic = {t: [q for q in pool if q["topic"] == t and q["difficulty"] == level] for t in topics}
        for lst in bucket_by_topic.values():
            rng.shuffle(lst)
        topic_cycle = topics[:]
        rng.shuffle(topic_cycle)
        pointers = {t: 0 for t in topics}
        taken = []
        idx = 0
        while len(taken) < target and any(pointers[t] < len(bucket_by_topic[t]) for t in topics):
            t = topic_cycle[idx % len(topic_cycle)]
            idx += 1
            if pointers[t] < len(bucket_by_topic[t]):
                taken.append(bucket_by_topic[t][pointers[t]])
                pointers[t] += 1
        result.extend(taken)

    total_target = easy_n + medium_n + hard_n
    if len(result) < total_target:
        chosen_ids = {id(q) for q in result}
        leftover = [q for q in pool if id(q) not in chosen_ids]
        rng.shuffle(leftover)
        result.extend(leftover[: total_target - len(result)])

    rng.shuffle(result)
    return result


def select_by_difficulty(pool, easy_n, medium_n, hard_n, rng):
    """Pick a target number of questions per difficulty bucket, backfilling from
    other buckets if one runs short, so the caller reliably gets easy_n+medium_n+hard_n
    questions (as long as the pool is large enough overall)."""
    pool = dedupe_pool(pool)
    buckets = {"easy": [], "medium": [], "hard": []}
    for q in pool:
        buckets[q["difficulty"]].append(q)
    for b in buckets.values():
        rng.shuffle(b)

    targets = {"easy": easy_n, "medium": medium_n, "hard": hard_n}
    result = []
    leftover = []
    for level, n in targets.items():
        chosen = buckets[level][:n]
        result.extend(chosen)
        leftover.extend(buckets[level][n:])

    total_target = easy_n + medium_n + hard_n
    if len(result) < total_target:
        rng.shuffle(leftover)
        result.extend(leftover[: total_target - len(result)])

    rng.shuffle(result)
    return result[:total_target]
