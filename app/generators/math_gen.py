"""Generates a large pool of TEKS Grade 5 Math questions with computed (guaranteed
correct) answers, then selects ~300 skewed toward medium/tricky difficulty.

Every answer is derived from actual arithmetic in this file rather than typed by
hand, so correctness follows from the math, not from careful transcription.
"""
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

from app.generators.common import make_question, select_balanced, fill_distractors

SEED = 20260819
SUBJECT = "math"

NUM_OPS = "Number & Operations"
ALGEBRA = "Algebraic Reasoning"
GEOMETRY = "Geometry & Measurement"
DATA = "Data Analysis"
FINANCE = "Personal Financial Literacy"


def _q2(x):
    """Quantize a Decimal to 2 places, formatted like 4.05 (no trailing 0 dropped)."""
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _fmt_dec(x, places):
    return str(x.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def _fmt_money(x):
    return f"${_q2(x):,.2f}"


def _fmt_int(n):
    return f"{n:,}"


def _fmt_frac(fr):
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"


# ---------------------------------------------------------------- Number & Operations

def gen_round_number(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        digits = rng.randint(4, 6)
        num = rng.randint(10 ** (digits - 1), 10 ** digits - 1)
        place = rng.choice([10, 100, 1000])
        key = (num, place)
        if key in seen:
            continue
        seen.add(key)

        remainder = num % place
        half = place // 2
        rounded_down = num - remainder
        rounded_up = rounded_down + place
        rounded = rounded_up if remainder >= half else rounded_down

        if remainder == half:
            difficulty = "hard"
        elif place == 10:
            difficulty = "easy"
        else:
            difficulty = "medium"

        qtext = f"Round {_fmt_int(num)} to the nearest {place}."
        correct = _fmt_int(rounded)
        base = [_fmt_int(rounded_down), _fmt_int(rounded_up), _fmt_int(num)]
        distractors = fill_distractors(
            base, correct,
            lambda i: _fmt_int(rounded + rng.choice([-place, place, -2 * place, 2 * place]) * (1 + i // 4)),
        )
        if len(distractors) < 3:
            continue
        explanation = (
            f"{_fmt_int(num)} is between {_fmt_int(rounded_down)} and {_fmt_int(rounded_up)}. "
            f"Since the digit being checked "
            f"{'is 5 or more' if remainder >= half else 'is less than 5'}, it rounds to {correct}."
        )
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_add_sub_decimals(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        places = rng.choice([1, 1, 2, 2, 3])
        scale = Decimal(1).scaleb(-places)
        a = Decimal(rng.randint(10, 9999)).scaleb(-places)
        b = Decimal(rng.randint(10, 9999)).scaleb(-places)
        op = rng.choice(["+", "-"])
        if op == "-" and b > a:
            a, b = b, a
        key = (float(a), float(b), op)
        if key in seen:
            continue
        seen.add(key)

        result = a + b if op == "+" else a - b
        correct = _fmt_dec(result, places)
        difficulty = "easy" if places == 1 else ("medium" if places == 2 else "hard")

        wrong_op_result = a - b if op == "+" else a + b
        base = [_fmt_dec(wrong_op_result, places), _fmt_dec(result + scale * 10, places)]

        def candidate(i, result=result, scale=scale, places=places):
            alt = result + Decimal(rng.choice([1, -1, 2, -2, 5, -5])) * scale * (1 + i // 6)
            return _fmt_dec(alt if alt >= 0 else -alt, places)

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue

        word = "sum" if op == "+" else "difference"
        qtext = f"What is {_fmt_dec(a, places)} {op} {_fmt_dec(b, places)}?"
        explanation = f"Line up the decimal points and {'add' if op == '+' else 'subtract'}: the {word} is {correct}."
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_multiply_decimals(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        mode = rng.choice(["dec_whole", "dec_dec"])
        if mode == "dec_whole":
            places = rng.choice([1, 2])
            a = Decimal(rng.randint(11, 99)).scaleb(-places)
            b = rng.randint(2, 12)
            difficulty = "easy" if places == 1 else "medium"
            qtext = f"What is {_fmt_dec(a, places)} x {b}?"
            key = (float(a), b)
        else:
            places_a, places_b = rng.choice([(1, 1), (1, 2), (2, 1)])
            a = Decimal(rng.randint(2, 99)).scaleb(-places_a)
            b = Decimal(rng.randint(2, 99)).scaleb(-places_b)
            places = places_a + places_b
            difficulty = "hard"
            qtext = f"What is {_fmt_dec(a, places_a)} x {_fmt_dec(b, places_b)}?"
            key = (float(a), float(b))

        if key in seen:
            continue
        seen.add(key)

        raw_result = a * b
        result = raw_result.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
        correct = _fmt_dec(result, places)

        b_dec = b if isinstance(b, Decimal) else Decimal(b)
        base = [_fmt_dec(result + Decimal("0.1"), places), _fmt_dec(a + b_dec, places)]

        def candidate(i, result=result, places=places):
            alt = result + Decimal(rng.choice([1, -1, 2, -2, 3, -3])).scaleb(-places) * (1 + i // 6)
            if alt < 0:
                return None
            return _fmt_dec(alt, places)

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue

        explanation = f"Multiply as if there were no decimal points, then place the decimal point: {correct}."
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_divide_whole(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        divisor = rng.randint(3, 12)
        quotient = rng.randint(6, 90)
        dividend = divisor * quotient
        key = (dividend, divisor)
        if key in seen:
            continue
        seen.add(key)

        difficulty = "easy" if dividend < 100 else ("medium" if dividend < 500 else "hard")
        qtext = f"What is {dividend} divided by {divisor}?"
        correct = str(quotient)
        base = [str(quotient + divisor)]

        def candidate(i, quotient=quotient):
            alt = quotient + rng.choice([-3, -2, -1, 1, 2, 3]) * (1 + i // 6)
            return str(alt) if alt > 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        explanation = f"{divisor} x {quotient} = {dividend}, so {dividend} / {divisor} = {quotient}."
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, difficulty, rng))
    return out


_DENOMS = [2, 3, 4, 5, 6, 8, 10, 12]


def gen_fraction_add_sub(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 10:
        attempts += 1
        same_denom = rng.random() < 0.35
        d1 = rng.choice(_DENOMS)
        d2 = d1 if same_denom else rng.choice(_DENOMS)
        n1 = rng.randint(1, d1 - 1)
        n2 = rng.randint(1, d2 - 1)
        f1 = Fraction(n1, d1)
        f2 = Fraction(n2, d2)
        op = rng.choice(["+", "-"])
        if op == "-" and f2 > f1:
            f1, f2 = f2, f1
        if op == "-" and f1 == f2:
            continue
        key = (f1, f2, op)
        if key in seen:
            continue
        seen.add(key)

        result = f1 + f2 if op == "+" else f1 - f2
        correct = _fmt_frac(result)
        difficulty = "easy" if same_denom else ("hard" if result.denominator > 12 else "medium")

        wrong_op = f1 - f2 if op == "+" else f1 + f2
        wrong_op = wrong_op if wrong_op.numerator >= 0 else -wrong_op
        no_common_denom = Fraction(n1 + n2, d1 + d2) if op == "+" else Fraction(abs(n1 - n2), max(d1, 1))
        base = [_fmt_frac(wrong_op), _fmt_frac(no_common_denom)]

        def candidate(i, result=result):
            step = 1 + i // 3
            offset = rng.choice([-2, -1, 1, 2]) * step
            new_num = result.numerator + offset
            if new_num <= 0:
                return None
            return _fmt_frac(Fraction(new_num, result.denominator))

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue

        qtext = f"What is {_fmt_frac(f1)} {op} {_fmt_frac(f2)}?"
        explanation = (
            f"{'Since the denominators already match, ' if same_denom else 'Find a common denominator, then '}"
            f"{'add' if op == '+' else 'subtract'} the numerators: {correct}."
        )
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_fraction_multiply(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 10:
        attempts += 1
        mode = rng.choice(["frac_whole", "frac_frac"])
        d1 = rng.choice(_DENOMS)
        n1 = rng.randint(1, d1 - 1)
        f1 = Fraction(n1, d1)
        if mode == "frac_whole":
            whole = rng.randint(2, 8)
            result = f1 * whole
            qtext = f"What is {_fmt_frac(f1)} x {whole}?"
            difficulty = "medium"
            key = (f1, whole, "w")
        else:
            d2 = rng.choice(_DENOMS)
            n2 = rng.randint(1, d2 - 1)
            f2 = Fraction(n2, d2)
            result = f1 * f2
            qtext = f"What is {_fmt_frac(f1)} x {_fmt_frac(f2)}?"
            difficulty = "hard"
            key = (f1, f2, "f")

        if key in seen:
            continue
        seen.add(key)

        correct = _fmt_frac(result)
        base = [_fmt_frac(Fraction(result.numerator + result.denominator, result.denominator))]

        def candidate(i, result=result):
            step = 1 + i // 3
            offset = rng.choice([-3, -2, -1, 1, 2, 3]) * step
            new_num = result.numerator + offset
            if new_num <= 0:
                return None
            return _fmt_frac(Fraction(new_num, result.denominator))

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue

        explanation = "Multiply the numerators together and the denominators together, then simplify if you can."
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_equivalent_fraction(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        d1 = rng.choice([2, 3, 4, 5, 6])
        n1 = rng.randint(1, d1 - 1)
        mult = rng.randint(2, 6)
        key = (n1, d1, mult)
        if key in seen:
            continue
        seen.add(key)

        n2, d2 = n1 * mult, d1 * mult
        correct = f"{n2}/{d2}"
        qtext = f"Which fraction is equivalent to {n1}/{d1}?"
        base = [f"{n2 + 1}/{d2}", f"{n2}/{d2 + mult}", f"{n1 + 1}/{d1 + 1}"]

        def candidate(i, n2=n2, d2=d2):
            return f"{n2 + rng.choice([-2, -1, 1, 2]) * (1 + i // 4)}/{d2}"

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        explanation = f"Multiply both the numerator and denominator of {n1}/{d1} by {mult} to get {correct}."
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, "medium", rng))
    return out


def gen_compare_numbers(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        places = rng.choice([1, 2])
        a = Decimal(rng.randint(10, 999)).scaleb(-places)
        b = Decimal(rng.randint(10, 999)).scaleb(-places)
        if a == b:
            continue
        key = (float(a), float(b))
        if key in seen:
            continue
        seen.add(key)

        bigger = a if a > b else b
        qtext = f"Which number is greater: {_fmt_dec(a, places)} or {_fmt_dec(b, places)}?"
        correct = _fmt_dec(bigger, places)
        smaller = a if a < b else b
        distractors = [_fmt_dec(smaller, places), "They are equal", "Cannot be determined"]
        difficulty = "easy" if abs(a - b) >= Decimal("1") else "hard"
        explanation = f"Compare digit by digit from the left: {correct} is larger."
        out.append(make_question(SUBJECT, NUM_OPS, qtext, correct, distractors, explanation, difficulty, rng))
    return out


# ---------------------------------------------------------------- Algebraic Reasoning

def gen_evaluate_expression(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        a, b, c = rng.randint(2, 12), rng.randint(2, 12), rng.randint(2, 12)
        pattern = rng.choice(["mul_add_paren", "add_mul", "sub_mul_paren", "mul_sub"])
        if pattern == "mul_add_paren":
            expr = f"{a} x ({b} + {c})"
            correct_val = a * (b + c)
            wrong_val = a * b + c
            difficulty = "medium"
        elif pattern == "add_mul":
            expr = f"{a} + {b} x {c}"
            correct_val = a + b * c
            wrong_val = (a + b) * c
            difficulty = "hard"
        elif pattern == "sub_mul_paren":
            sub = rng.randint(1, 5)
            expr = f"({a} + {b}) x {c} - {sub}"
            correct_val = (a + b) * c - sub
            wrong_val = a + b * c - sub
            difficulty = "hard"
        else:
            expr = f"{a} x {b} - {c}"
            correct_val = a * b - c
            wrong_val = a * (b - c)
            difficulty = "medium"

        key = expr
        if key in seen:
            continue
        seen.add(key)

        correct = str(correct_val)
        base = [str(wrong_val)]

        def candidate(i, correct_val=correct_val):
            alt = correct_val + rng.choice([-3, -2, -1, 1, 2, 3]) * (1 + i // 6)
            return str(alt) if alt >= 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        qtext = f"What is the value of {expr}?"
        explanation = "Follow the order of operations: solve inside parentheses first, then multiply/divide, then add/subtract."
        out.append(make_question(SUBJECT, ALGEBRA, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_solve_equation(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        op = rng.choice(["+", "-", "x", "/"])
        n = rng.randint(2, 20)
        if op == "+":
            a = rng.randint(2, 50)
            b = a + n
            qtext = f"What is the value of n if n + {a} = {b}?"
            difficulty = "easy"
        elif op == "-":
            a = rng.randint(2, 50)
            b = n
            n = b + a
            qtext = f"What is the value of n if n - {a} = {b}?"
            difficulty = "medium"
        elif op == "x":
            a = rng.randint(2, 9)
            b = a * n
            qtext = f"What is the value of n if n x {a} = {b}?"
            difficulty = "medium"
        else:
            a = rng.randint(2, 9)
            b = n
            n = b * a
            qtext = f"What is the value of n if n / {a} = {b}?"
            difficulty = "hard"

        key = qtext
        if key in seen:
            continue
        seen.add(key)

        correct = str(n)
        base = [str(n + a if op in ("+", "x") else n - a)]

        def candidate(i, n=n):
            alt = n + rng.choice([-3, -2, -1, 1, 2, 3]) * (1 + i // 6)
            return str(alt) if alt > 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        explanation = "Use the inverse operation on both sides of the equation to isolate n."
        out.append(make_question(SUBJECT, ALGEBRA, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_number_pattern(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        start = rng.randint(1, 20)
        step = rng.randint(2, 12)
        op = rng.choice(["add", "sub"])
        terms = []
        val = start
        for _ in range(4):
            terms.append(val)
            val = val + step if op == "add" else val - step
        if op == "sub" and val < 0:
            continue
        key = (start, step, op)
        if key in seen:
            continue
        seen.add(key)

        next_val = val
        correct = str(next_val)
        sequence_str = ", ".join(str(t) for t in terms)
        qtext = f"What is the next number in the pattern: {sequence_str}, ___?"
        base = [str(terms[-1] + (step - 1 if step > 1 else step + 1))]

        def candidate(i, next_val=next_val, step=step):
            alt = next_val + rng.choice([-2, -1, 1, 2]) * (1 + i // 4)
            return str(alt) if alt >= 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        difficulty = "easy" if step <= 5 else "medium"
        explanation = f"The rule is '{'add' if op == 'add' else 'subtract'} {step}' each time, so the next number is {correct}."
        out.append(make_question(SUBJECT, ALGEBRA, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_input_output_rule(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        mult = rng.randint(2, 6)
        add = rng.randint(0, 10)
        x = rng.randint(2, 15)
        key = (mult, add, x)
        if key in seen:
            continue
        seen.add(key)

        y = mult * x + add
        rule_str = f"multiply by {mult}" + (f", then add {add}" if add else "")
        qtext = f"A rule says: {rule_str}. What is the output when the input is {x}?"
        correct = str(y)
        base = [str(mult * x), str((x + add) * mult)]

        def candidate(i, y=y, mult=mult):
            alt = y + rng.choice([-3, -2, -1, 1, 2, 3]) * mult * (1 + i // 6) // max(mult, 1)
            alt = y + rng.choice([-3, -2, -1, 1, 2, 3]) * (1 + i // 6)
            return str(alt) if alt > 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        difficulty = "medium" if add else "easy"
        if mult >= 5 and add:
            difficulty = "hard"
        explanation = f"Apply the rule in order: {x} x {mult}" + (f" + {add}" if add else "") + f" = {correct}."
        out.append(make_question(SUBJECT, ALGEBRA, qtext, correct, distractors, explanation, difficulty, rng))
    return out


# ---------------------------------------------------------------- Geometry & Measurement

def gen_area_perimeter_rectangle(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        length = rng.randint(3, 24)
        width = rng.randint(2, 20)
        if length == width and rng.random() < 0.5:
            continue
        unit = rng.choice(["cm", "in", "m", "ft"])
        ask_area = rng.random() < 0.6
        key = (length, width, unit, ask_area)
        if key in seen:
            continue
        seen.add(key)

        suffix = "²" if ask_area else ""
        if ask_area:
            correct_val = length * width
            qtext = f"What is the area of a rectangle with a length of {length} {unit} and a width of {width} {unit}?"
            correct = f"{correct_val} {unit}²"
            wrong_val = 2 * (length + width)
            explanation = f"Area = length x width = {length} x {width} = {correct_val} {unit}²."
        else:
            correct_val = 2 * (length + width)
            qtext = f"What is the perimeter of a rectangle with a length of {length} {unit} and a width of {width} {unit}?"
            correct = f"{correct_val} {unit}"
            wrong_val = length * width
            explanation = f"Perimeter = 2 x (length + width) = 2 x ({length} + {width}) = {correct_val} {unit}."

        base = [f"{wrong_val} {unit}{suffix}"]

        def candidate(i, correct_val=correct_val, unit=unit, suffix=suffix):
            alt = correct_val + rng.choice([-4, -3, -2, 2, 3, 4]) * (1 + i // 6)
            return f"{alt} {unit}{suffix}" if alt > 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        difficulty = "easy" if max(length, width) <= 12 else "medium"
        out.append(make_question(SUBJECT, GEOMETRY, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_volume_prism(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        l, w, h = rng.randint(2, 12), rng.randint(2, 12), rng.randint(2, 12)
        unit = rng.choice(["cm", "in", "m", "ft"])
        key = (l, w, h, unit)
        if key in seen:
            continue
        seen.add(key)

        vol = l * w * h
        qtext = f"What is the volume of a rectangular prism with length {l} {unit}, width {w} {unit}, and height {h} {unit}?"
        correct = f"{vol} {unit}³"
        wrong_val = 2 * (l + w + h)
        base = [f"{wrong_val} {unit}³"]

        def candidate(i, vol=vol, unit=unit):
            alt = vol + rng.choice([-6, -4, -3, 3, 4, 6]) * (1 + i // 6)
            return f"{alt} {unit}³" if alt > 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        difficulty = "easy" if max(l, w, h) <= 6 else ("medium" if max(l, w, h) <= 10 else "hard")
        explanation = f"Volume = length x width x height = {l} x {w} x {h} = {vol} {unit}³."
        out.append(make_question(SUBJECT, GEOMETRY, qtext, correct, distractors, explanation, difficulty, rng))
    return out


_QUADRILATERALS = [
    ("square", "4 equal sides and 4 right angles", "easy"),
    ("rectangle", "4 right angles and 2 pairs of equal, parallel sides", "easy"),
    ("rhombus", "4 equal sides with opposite sides parallel, but no right angles required", "medium"),
    ("trapezoid", "exactly one pair of parallel sides", "medium"),
    ("parallelogram", "2 pairs of parallel sides and opposite sides equal in length", "hard"),
]
_TRIANGLES = [
    ("equilateral triangle", "3 sides of equal length and 3 equal angles", "easy"),
    ("isosceles triangle", "exactly 2 sides of equal length", "medium"),
    ("scalene triangle", "no sides of equal length", "medium"),
    ("right triangle", "one 90-degree angle", "easy"),
]
_SOLIDS = [
    ("cube", 6, 12, 8),
    ("rectangular prism", 6, 12, 8),
    ("triangular prism", 5, 9, 6),
    ("square pyramid", 5, 8, 5),
]


def gen_shape_classification(rng, target):
    out = []
    seen = set()
    pool = [("desc", name, desc, difficulty) for name, desc, difficulty in _QUADRILATERALS + _TRIANGLES]
    pool += [("faces", name, faces, edges, vertices) for name, faces, edges, vertices in _SOLIDS]

    attempts = 0
    while len(out) < target and attempts < target * 12:
        attempts += 1
        item = rng.choice(pool)
        if item[0] == "desc":
            _, name, desc, difficulty = item
            others = [n for n, d, diff in (_QUADRILATERALS + _TRIANGLES) if n != name]
            distractors = rng.sample(others, 3)
            qtext = f"Which shape has {desc}?"
            key = qtext
            if key in seen:
                continue
            seen.add(key)
            explanation = f"A {name} is defined by having {desc}."
            out.append(make_question(SUBJECT, GEOMETRY, qtext, name, distractors, explanation, difficulty, rng))
        else:
            _, name, faces, edges, vertices = item
            ask = rng.choice(["faces", "edges", "vertices"])
            value = {"faces": faces, "edges": edges, "vertices": vertices}[ask]
            key = (name, ask)
            if key in seen:
                continue
            seen.add(key)
            qtext = f"How many {ask} does a {name} have?"
            correct = str(value)
            distractors = [str(value + 1), str(max(value - 1, 0)), str(value + 2)]
            distractors = [d for d in dict.fromkeys(distractors) if d != correct][:3]
            if len(distractors) < 3:
                continue
            difficulty = "easy" if name in ("cube", "rectangular prism") else "medium"
            explanation = f"A {name} has {faces} faces, {edges} edges, and {vertices} vertices."
            out.append(make_question(SUBJECT, GEOMETRY, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_angle_classification(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        degrees = rng.randint(5, 175)
        if degrees in seen:
            continue
        seen.add(degrees)
        if degrees == 90:
            correct = "Right angle"
        elif degrees < 90:
            correct = "Acute angle"
        else:
            correct = "Obtuse angle"
        options = ["Acute angle", "Right angle", "Obtuse angle", "Straight angle"]
        distractors = [o for o in options if o != correct][:3]
        qtext = f"An angle measures {degrees} degrees. What type of angle is it?"
        difficulty = "hard" if 80 <= degrees <= 100 and degrees != 90 else "easy"
        explanation = (
            "A right angle is exactly 90 degrees, an acute angle is less than 90 degrees, "
            f"and an obtuse angle is more than 90 (but less than 180) degrees — {degrees} degrees is a {correct.lower()}."
        )
        out.append(make_question(SUBJECT, GEOMETRY, qtext, correct, distractors, explanation, difficulty, rng))
    return out


_CONVERSIONS = [
    ("feet", "inches", 12),
    ("yards", "feet", 3),
    ("pounds", "ounces", 16),
    ("meters", "centimeters", 100),
    ("kilometers", "meters", 1000),
    ("kilograms", "grams", 1000),
    ("liters", "milliliters", 1000),
]


def gen_unit_conversion(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        from_unit, to_unit, factor = rng.choice(_CONVERSIONS)
        amount = rng.randint(2, 12)
        key = (from_unit, to_unit, amount)
        if key in seen:
            continue
        seen.add(key)

        result = amount * factor
        qtext = f"How many {to_unit} are in {amount} {from_unit}?"
        correct = _fmt_int(result)
        base = [_fmt_int(amount + factor)]

        def candidate(i, result=result, factor=factor):
            step = max(factor // 4, 1) * (1 + i // 5)
            alt = result + rng.choice([-2, -1, 1, 2]) * step
            return _fmt_int(alt) if alt > 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        difficulty = "medium" if factor <= 16 else "hard"
        unit_singular = from_unit[:-1] if from_unit.endswith("s") else from_unit
        explanation = f"There are {factor} {to_unit} in 1 {unit_singular}, so {amount} x {factor} = {result}."
        out.append(make_question(SUBJECT, GEOMETRY, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_coordinate_point(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        x, y = rng.randint(0, 12), rng.randint(0, 12)
        key = (x, y)
        if key in seen:
            continue
        seen.add(key)
        ask_x = rng.random() < 0.5
        correct = str(x if ask_x else y)
        qtext = f"On a coordinate grid, what is the {'x' if ask_x else 'y'}-coordinate of the point ({x}, {y})?"
        other = y if ask_x else x
        distractors = [str(other), str(int(correct) + 1), str(max(int(correct) - 1, 0))]
        distractors = [d for d in dict.fromkeys(distractors) if d != correct][:3]
        if len(distractors) < 3:
            continue
        explanation = "In an ordered pair (x, y), the first number is the x-coordinate and the second is the y-coordinate."
        out.append(make_question(SUBJECT, GEOMETRY, qtext, correct, distractors, explanation, "easy", rng))
    return out


# ---------------------------------------------------------------- Data Analysis

def gen_mean_median_mode_range(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 12:
        attempts += 1
        n_count = rng.choice([5, 5, 6, 7])
        data = sorted(rng.randint(1, 30) for _ in range(n_count))
        key = tuple(data)
        if key in seen:
            continue
        seen.add(key)

        stat = rng.choice(["mean", "median", "range", "mode"])
        data_str = ", ".join(str(d) for d in data)

        if stat == "mean":
            total = sum(data)
            if total % n_count != 0:
                continue
            correct_val = total // n_count
            difficulty = "medium"
            explanation = f"Add all the numbers ({total}) and divide by how many there are ({n_count}): {correct_val}."
        elif stat == "median":
            mid = n_count // 2
            if n_count % 2 == 1:
                correct_val = data[mid]
                difficulty = "medium"
            else:
                if (data[mid - 1] + data[mid]) % 2 != 0:
                    continue
                correct_val = (data[mid - 1] + data[mid]) // 2
                difficulty = "hard"
            explanation = f"Order the numbers and find the middle value: the median is {correct_val}."
        elif stat == "range":
            correct_val = data[-1] - data[0]
            difficulty = "easy"
            explanation = f"Range = greatest value - least value = {data[-1]} - {data[0]} = {correct_val}."
        else:
            counts = {}
            for d in data:
                counts[d] = counts.get(d, 0) + 1
            max_count = max(counts.values())
            if max_count < 2:
                continue
            correct_val = max(k for k, v in counts.items() if v == max_count)
            difficulty = "easy"
            explanation = f"The mode is the value that appears most often: {correct_val}."

        correct = str(correct_val)
        base = [str(data[0]), str(data[-1])]

        def candidate(i, correct_val=correct_val):
            alt = correct_val + rng.choice([-3, -2, -1, 1, 2, 3]) * (1 + i // 6)
            return str(alt) if alt >= 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        qtext = f"What is the {stat} of this data set: {data_str}?"
        out.append(make_question(SUBJECT, DATA, qtext, correct, distractors, explanation, difficulty, rng))
    return out


_SURVEY_ITEMS = [
    ("pets owned", ["0 pets", "1 pet", "2 pets", "3 pets"]),
    ("favorite season", ["Spring", "Summer", "Fall", "Winter"]),
    ("books read this month", ["0-1 books", "2-3 books", "4-5 books", "6+ books"]),
    ("favorite lunch", ["Pizza", "Tacos", "Salad", "Sandwich"]),
]


def gen_frequency_table(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        topic_label, categories = rng.choice(_SURVEY_ITEMS)
        counts = [rng.randint(2, 12) for _ in categories]
        key = (topic_label, tuple(counts))
        if key in seen:
            continue
        seen.add(key)

        table_str = "; ".join(f"{c}: {n} students" for c, n in zip(categories, counts))
        total = sum(counts)
        question_type = rng.choice(["total", "most", "least", "difference"])

        if question_type == "total":
            correct_val = total
            qtext = f"A class was surveyed about {topic_label}: {table_str}. How many students were surveyed in total?"
            explanation = f"Add all the group totals: {' + '.join(str(c) for c in counts)} = {total}."
            difficulty = "easy"
        elif question_type == "most":
            best_idx = counts.index(max(counts))
            correct_val = categories[best_idx]
            qtext = f"A class was surveyed about {topic_label}: {table_str}. Which choice got the most responses?"
            explanation = f"{categories[best_idx]} has the highest count, {max(counts)}."
            difficulty = "easy"
        elif question_type == "least":
            worst_idx = counts.index(min(counts))
            correct_val = categories[worst_idx]
            qtext = f"A class was surveyed about {topic_label}: {table_str}. Which choice got the fewest responses?"
            explanation = f"{categories[worst_idx]} has the lowest count, {min(counts)}."
            difficulty = "medium"
        else:
            best_idx = counts.index(max(counts))
            worst_idx = counts.index(min(counts))
            if best_idx == worst_idx:
                continue
            correct_val = max(counts) - min(counts)
            qtext = (
                f"A class was surveyed about {topic_label}: {table_str}. How many more students chose "
                f"{categories[best_idx]} than {categories[worst_idx]}?"
            )
            explanation = f"{max(counts)} - {min(counts)} = {correct_val}."
            difficulty = "hard"

        correct = str(correct_val)
        if question_type in ("most", "least"):
            distractors = [c for c in categories if c != correct_val][:3]
        else:
            distractors = [str(correct_val + 1), str(max(correct_val - 1, 0)), str(correct_val + 2)]
            distractors = [d for d in dict.fromkeys(distractors) if d != correct][:3]
        if len(distractors) < 3:
            continue
        out.append(make_question(SUBJECT, DATA, qtext, correct, distractors, explanation, difficulty, rng))
    return out


# ---------------------------------------------------------------- Personal Financial Literacy

_ITEMS = [
    ("book", 6, 15), ("toy robot", 8, 25), ("backpack", 12, 40), ("board game", 10, 30),
    ("water bottle", 3, 12), ("basketball", 9, 22), ("art set", 7, 20), ("puzzle", 5, 18),
]


def gen_making_change(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        item, low, high = rng.choice(_ITEMS)
        price = _q2(Decimal(rng.randint(low * 100, high * 100)) / 100)
        paid = Decimal(rng.choice([10, 15, 20, 25, 30, 50]))
        if paid <= price:
            continue
        key = (item, price)
        if key in seen:
            continue
        seen.add(key)

        change = _q2(paid - price)
        qtext = f"A {item} costs {_fmt_money(price)}. You pay with a {_fmt_money(paid)} bill. How much change should you get?"
        correct = _fmt_money(change)
        base = [_fmt_money(_q2(paid + price))]

        def candidate(i, change=change):
            alt = _q2(change + Decimal(rng.choice([-2, -1, 1, 2])) * Decimal("0.50") * (1 + i // 4))
            return _fmt_money(alt) if alt > 0 else None

        distractors = fill_distractors(base, correct, candidate)
        if len(distractors) < 3:
            continue
        difficulty = "medium" if change.as_tuple().exponent == -2 else "easy"
        explanation = f"{_fmt_money(paid)} - {_fmt_money(price)} = {correct}."
        out.append(make_question(SUBJECT, FINANCE, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_unit_price_comparison(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        item = rng.choice(["juice boxes", "granola bars", "pencils", "markers", "erasers", "notebooks"])
        count_a, count_b = rng.sample([4, 5, 6, 8, 10, 12], 2)
        price_a = Decimal(rng.randint(200, 900)) / 100
        price_b = Decimal(rng.randint(200, 900)) / 100
        unit_a = _q2(price_a / count_a)
        unit_b = _q2(price_b / count_b)
        if unit_a == unit_b:
            continue
        key = (item, count_a, count_b, price_a, price_b)
        if key in seen:
            continue
        seen.add(key)

        better = "Pack A" if unit_a < unit_b else "Pack B"
        qtext = (
            f"Pack A has {count_a} {item} for {_fmt_money(price_a)}. Pack B has {count_b} {item} for {_fmt_money(price_b)}. "
            f"Which pack is the better deal (lower price per item)?"
        )
        correct = better
        other = "Pack B" if better == "Pack A" else "Pack A"
        distractors = [other, "Both cost the same per item", "Cannot be determined"]
        difficulty = "hard" if abs(unit_a - unit_b) < Decimal("0.10") else "medium"
        explanation = (
            f"Pack A costs {_fmt_money(unit_a)} per item and Pack B costs {_fmt_money(unit_b)} per item, "
            f"so {better} has the lower price per item."
        )
        out.append(make_question(SUBJECT, FINANCE, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def gen_budget_savings(rng, target):
    out, seen, attempts = [], set(), 0
    while len(out) < target and attempts < target * 8:
        attempts += 1
        mode = rng.choice(["budget", "saving_weeks", "total_cost"])
        if mode == "budget":
            income = rng.randint(20, 60)
            expense_a = rng.randint(5, income // 2)
            expense_b = rng.randint(3, income // 3)
            if expense_a + expense_b >= income:
                continue
            key = (mode, income, expense_a, expense_b)
            if key in seen:
                continue
            seen.add(key)
            savings = income - expense_a - expense_b
            qtext = (
                f"Jordan earns ${income} doing chores this month. Jordan spends ${expense_a} on a gift and "
                f"${expense_b} on snacks. How much money does Jordan have left to save?"
            )
            correct = f"${savings}"
            distractors = [f"${savings + 5}", f"${income - expense_a}", f"${max(savings - 5, 0)}"]
            difficulty = "medium"
            explanation = f"${income} - ${expense_a} - ${expense_b} = ${savings}."
        elif mode == "saving_weeks":
            per_week = rng.choice([2, 3, 4, 5, 6, 8])
            weeks = rng.randint(4, 12)
            key = (mode, per_week, weeks)
            if key in seen:
                continue
            seen.add(key)
            total = per_week * weeks
            qtext = f"Sam saves ${per_week} every week. How much will Sam have saved after {weeks} weeks?"
            correct = f"${total}"
            distractors = [f"${total + per_week}", f"${per_week + weeks}", f"${max(total - per_week, 0)}"]
            difficulty = "easy" if weeks <= 6 else "medium"
            explanation = f"${per_week} x {weeks} weeks = ${total}."
        else:
            item, low, high = rng.choice(_ITEMS)
            price = rng.randint(low, high)
            qty = rng.randint(2, 5)
            key = (mode, item, price, qty)
            if key in seen:
                continue
            seen.add(key)
            total = price * qty
            qtext = f"Each {item} costs ${price}. What is the total cost of buying {qty} of them?"
            correct = f"${total}"
            distractors = [f"${total + price}", f"${price + qty}", f"${max(total - price, 0)}"]
            difficulty = "easy"
            explanation = f"${price} x {qty} = ${total}."

        distractors = [d for d in dict.fromkeys(distractors) if d != correct][:3]
        if len(distractors) < 3:
            continue
        out.append(make_question(SUBJECT, FINANCE, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def generate_math_questions(total=300, easy_ratio=0.2, medium_ratio=0.5, hard_ratio=0.3):
    rng = random.Random(SEED)
    pool = []
    pool += gen_round_number(rng, 45)
    pool += gen_add_sub_decimals(rng, 45)
    pool += gen_multiply_decimals(rng, 35)
    pool += gen_divide_whole(rng, 35)
    pool += gen_fraction_add_sub(rng, 40)
    pool += gen_fraction_multiply(rng, 25)
    pool += gen_equivalent_fraction(rng, 20)
    pool += gen_compare_numbers(rng, 20)
    pool += gen_evaluate_expression(rng, 35)
    pool += gen_solve_equation(rng, 35)
    pool += gen_number_pattern(rng, 25)
    pool += gen_input_output_rule(rng, 25)
    pool += gen_area_perimeter_rectangle(rng, 35)
    pool += gen_volume_prism(rng, 25)
    pool += gen_shape_classification(rng, 20)
    pool += gen_angle_classification(rng, 20)
    pool += gen_unit_conversion(rng, 25)
    pool += gen_coordinate_point(rng, 15)
    pool += gen_mean_median_mode_range(rng, 60)
    pool += gen_frequency_table(rng, 40)
    pool += gen_making_change(rng, 30)
    pool += gen_unit_price_comparison(rng, 30)
    pool += gen_budget_savings(rng, 30)

    easy_n = round(total * easy_ratio)
    medium_n = round(total * medium_ratio)
    hard_n = total - easy_n - medium_n
    return select_balanced(pool, easy_n, medium_n, hard_n, rng)


if __name__ == "__main__":
    qs = generate_math_questions()
    from collections import Counter
    print("total:", len(qs))
    print("by difficulty:", Counter(q["difficulty"] for q in qs))
    print("by topic:", Counter(q["topic"] for q in qs))
    for q in qs[:8]:
        print("-", q["question_text"], "=>", q["correct_choice"], q[f"choice_{q['correct_choice'].lower()}"])
