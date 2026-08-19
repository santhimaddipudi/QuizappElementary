"""Generates a large pool of TEKS Grade 5 Science questions from a curated,
hand-checked fact bank (category groups, term/definition clusters, and ordered
process sequences), then selects ~300 skewed toward medium/tricky difficulty.

Question TEXT is template-generated, but every underlying fact (which example
belongs to which category, each definition, each sequence order) is authored
here directly so accuracy doesn't depend on random generation.
"""
import random

from app.generators.common import make_question, select_balanced, fill_distractors

SEED = 20260819
SUBJECT = "science"

MATTER = "Matter and Energy"
FORCE = "Force, Motion, and Energy"
EARTH = "Earth and Space"
ORGANISMS = "Organisms and Environments"
INVESTIGATION = "Scientific Investigation"

# ---------------------------------------------------------------------------
# Category groups: { group_key: (topic, base_difficulty, {category: [examples]}) }
# Used for "Which of these is an example of X?" / "...is NOT an example of X?"
# ---------------------------------------------------------------------------
CATEGORY_GROUPS = {
    "states_of_matter": (MATTER, "easy", {
        "a solid": ["an ice cube", "a wooden block", "a brick", "a coin", "a glass marble", "a rock", "a book"],
        "a liquid": ["milk", "vegetable oil", "maple syrup", "vinegar", "juice", "rain water"],
        "a gas": ["the oxygen we breathe", "helium in a balloon", "steam from a kettle", "water vapor in the air", "carbon dioxide"],
    }),
    "physical_vs_chemical_change": (MATTER, "medium", {
        "a physical change": ["melting ice", "freezing water", "cutting paper", "crumpling foil", "breaking a glass", "dissolving sugar in water", "boiling water into steam"],
        "a chemical change": ["burning wood", "a nail rusting", "baking a cake", "an egg cooking", "milk turning sour", "fireworks exploding", "mixing baking soda and vinegar to make bubbles"],
    }),
    "mixtures_vs_solutions": (MATTER, "medium", {
        "a mixture that can be separated by picking out the parts": ["trail mix", "a salad", "sand and water", "oil and water", "cereal with raisins"],
        "a solution where the parts are evenly dissolved": ["salt water", "sugar water", "lemonade", "a sports drink"],
    }),
    "conductors_vs_insulators": (MATTER, "medium", {
        "a good conductor of heat and electricity": ["a metal spoon", "a copper wire", "an aluminum can", "an iron nail"],
        "a good insulator (does not conduct well)": ["a wooden spoon", "a rubber band", "a plastic ruler", "a glass cup", "a foam cup"],
    }),
    "magnetic_vs_nonmagnetic": (MATTER, "easy", {
        "attracted to a magnet": ["an iron nail", "a steel paperclip", "a steel bolt"],
        "not attracted to a magnet": ["a plastic spoon", "a wooden block", "an aluminum can", "a rubber ball", "a glass marble"],
    }),
    "energy_forms": (FORCE, "easy", {
        "light energy": ["sunlight", "a flashlight beam", "a glowing light bulb"],
        "sound energy": ["a ringing bell", "a barking dog", "music from a speaker"],
        "thermal (heat) energy": ["a campfire", "a hot stove", "warm sunlight on skin"],
        "mechanical energy": ["a moving bicycle", "a spinning fan blade", "a rolling ball"],
    }),
    "potential_vs_kinetic": (FORCE, "medium", {
        "potential (stored) energy": ["a ball held up high before it's dropped", "a stretched rubber band", "water behind a dam", "a drawn bow before the arrow is released"],
        "kinetic (motion) energy": ["a rolling ball", "a flying bird", "a moving car", "wind blowing through trees"],
    }),
    "simple_machines": (FORCE, "medium", {
        "a lever": ["a seesaw", "a pair of scissors", "a crowbar"],
        "a pulley": ["a flagpole rope system", "a window blind cord", "a crane's lifting hook"],
        "a wheel and axle": ["a doorknob", "a steering wheel", "a bicycle wheel"],
        "an inclined plane": ["a wheelchair ramp", "a slide", "a mountain road"],
        "a wedge": ["an axe head", "a doorstop", "a knife blade"],
        "a screw": ["a jar lid", "a screw used in wood", "a spiral staircase"],
    }),
    "transparent_translucent_opaque": (FORCE, "medium", {
        "transparent (lets light pass clearly through)": ["a clear glass window", "clear plastic wrap", "still water"],
        "translucent (lets some light through, but blurry)": ["wax paper", "frosted glass", "a thin white curtain"],
        "opaque (blocks light completely)": ["a wooden door", "a brick wall", "a metal spoon"],
    }),
    "rock_types": (EARTH, "medium", {
        "an igneous rock (formed from cooled melted rock)": ["basalt", "granite", "obsidian", "pumice"],
        "a sedimentary rock (formed from layers of sediment)": ["sandstone", "limestone", "shale"],
        "a metamorphic rock (changed by heat and pressure)": ["marble", "slate", "gneiss"],
    }),
    "renewable_vs_nonrenewable": (EARTH, "medium", {
        "a renewable resource": ["wind", "sunlight", "flowing water", "trees that can be replanted"],
        "a nonrenewable resource": ["coal", "oil (petroleum)", "natural gas"],
    }),
    "producers_consumers_decomposers": (ORGANISMS, "easy", {
        "a producer (makes its own food from sunlight)": ["an oak tree", "grass", "a rose bush", "algae"],
        "a consumer (eats other organisms for food)": ["a rabbit", "a hawk", "a deer", "a human"],
        "a decomposer (breaks down dead plants and animals)": ["a mushroom", "a mold", "a earthworm", "bacteria in soil"],
    }),
    "inherited_vs_acquired_traits": (ORGANISMS, "hard", {
        "an inherited trait (passed down from parents)": ["eye color", "fur color in a puppy", "the shape of a leaf", "having four legs like its parents"],
        "an acquired or learned trait (not passed down)": ["knowing how to ride a bike", "a scar from a fall", "a trained trick a dog learns", "the language a person speaks"],
    }),
    "adaptation_type": (ORGANISMS, "hard", {
        "a physical adaptation (a body feature)": ["a polar bear's thick white fur", "a cactus's sharp spines", "a duck's webbed feet", "a giraffe's long neck"],
        "a behavioral adaptation (something an animal does)": ["birds migrating south for winter", "a bear hibernating all winter", "an owl hunting at night", "a squirrel storing nuts for winter"],
    }),
    "habitat_animals": (ORGANISMS, "medium", {
        "an animal well-adapted to the desert": ["a camel", "a desert tortoise", "a rattlesnake", "a scorpion"],
        "an animal well-adapted to the arctic": ["a polar bear", "an arctic fox", "a walrus", "a penguin"],
        "an animal well-adapted to the ocean": ["a dolphin", "a clownfish", "a sea turtle", "an octopus"],
    }),
    "measuring_tools": (INVESTIGATION, "medium", {
        "used for measuring temperature": ["a thermometer"],
        "used for measuring mass": ["a balance", "a scale"],
        "used for measuring length": ["a ruler", "a meter stick", "a measuring tape"],
        "used for measuring the volume of a liquid": ["a graduated cylinder", "a beaker"],
        "used for measuring time": ["a stopwatch"],
        "used for measuring wind speed": ["an anemometer"],
        "used for measuring rainfall": ["a rain gauge"],
    }),
}

# ---------------------------------------------------------------------------
# Term/definition clusters. Distractors are drawn from the same cluster so
# they're plausible (same topic area) rather than random unrelated words.
# ---------------------------------------------------------------------------
TERM_CLUSTERS = {
    "state_changes": (MATTER, "medium", {
        "Evaporation": "when a liquid changes into a gas",
        "Condensation": "when a gas changes into a liquid",
        "Freezing": "when a liquid changes into a solid",
        "Melting": "when a solid changes into a liquid",
    }),
    "forces": (FORCE, "medium", {
        "Gravity": "a force that pulls objects toward the center of the Earth",
        "Friction": "a force that slows down or stops objects that are rubbing together",
        "Magnetism": "a force that attracts certain metals, like iron and steel",
        "Inertia": "the tendency of an object to keep doing what it's already doing unless a force acts on it",
    }),
    "earth_processes": (EARTH, "hard", {
        "Weathering": "the breaking down of rock into smaller pieces over time",
        "Erosion": "the movement of weathered rock and soil from one place to another",
        "Deposition": "the dropping off of sediment that was being carried by water, wind, or ice",
        "Sediment": "small pieces of rock, sand, or soil that have been broken down and moved",
    }),
    "investigation_variables": (INVESTIGATION, "hard", {
        "Independent variable": "the one thing a scientist deliberately changes in an experiment",
        "Dependent variable": "what a scientist measures or observes to see if it was affected",
        "Controlled variable": "something kept exactly the same in every trial of an experiment",
        "Hypothesis": "a testable prediction made before running an experiment",
    }),
    "earth_layers": (EARTH, "medium", {
        "Crust": "Earth's thin, solid, outermost layer, where we live",
        "Mantle": "the thick, mostly solid layer beneath the crust, made of hot rock",
        "Core": "the layer at the very center of the Earth, made mostly of iron and nickel",
        "Atmosphere": "the layer of gases surrounding the Earth",
    }),
}

# ---------------------------------------------------------------------------
# Ordered process sequences, for "what comes next / before / first / last".
# ---------------------------------------------------------------------------
SEQUENCES = {
    "butterfly_life_cycle": (ORGANISMS, ["Egg", "Larva (caterpillar)", "Pupa (chrysalis)", "Adult butterfly"],
                              "butterfly life cycle"),
    "frog_life_cycle": (ORGANISMS, ["Egg", "Tadpole", "Tadpole with legs", "Adult frog"], "frog life cycle"),
    "plant_life_cycle": (ORGANISMS, ["Seed", "Germination (sprouting)", "Seedling", "Mature plant that flowers and makes new seeds"],
                          "plant life cycle"),
    "water_cycle": (EARTH, ["Evaporation (water rises as vapor)", "Condensation (vapor forms clouds)",
                             "Precipitation (rain or snow falls)", "Collection (water gathers in oceans, lakes, and rivers)"],
                    "water cycle"),
    "scientific_method": (INVESTIGATION, ["Ask a question", "Form a hypothesis", "Plan and conduct a test",
                                           "Record and analyze data", "Draw a conclusion"], "scientific method"),
}

# ---------------------------------------------------------------------------
# Hand-authored standalone facts that don't fit the patterns above cleanly.
# (subject-implicit: science) tuple = (topic, question, correct, distractors, explanation, difficulty)
# ---------------------------------------------------------------------------
DIRECT_FACTS = [
    (EARTH, "What causes day and night on Earth?", "Earth rotating on its axis",
     ["Earth revolving around the Sun", "The Moon orbiting Earth", "The Sun moving around Earth"],
     "Earth spins (rotates) on its axis about once every 24 hours, causing day and night.", "medium"),
    (EARTH, "What causes the four seasons on Earth?", "Earth's tilted axis as it revolves around the Sun",
     ["Earth spinning faster in summer", "The Moon blocking sunlight", "Clouds covering the Sun"],
     "As Earth orbits (revolves around) the Sun, its tilted axis changes how directly sunlight hits different parts of the planet, causing seasons.", "hard"),
    (EARTH, "About how long does it take Earth to complete one full rotation on its axis?", "About 24 hours",
     ["About 1 hour", "About 1 week", "About 1 year"],
     "One full spin of Earth on its axis takes about 24 hours, which we call one day.", "easy"),
    (EARTH, "About how long does it take Earth to complete one full revolution (orbit) around the Sun?", "About 365 days",
     ["About 24 hours", "About 30 days", "About 12 hours"],
     "It takes Earth about 365 days (one year) to fully orbit the Sun.", "medium"),
    (EARTH, "What is the main source of energy that powers the water cycle?", "The Sun",
     ["The Moon", "Wind", "The ocean floor"],
     "Heat from the Sun causes evaporation, which drives the entire water cycle.", "medium"),
    (EARTH, "Which layer of Earth do people live on?", "The crust", ["The mantle", "The outer core", "The inner core"],
     "The crust is Earth's thin, solid outermost layer.", "easy"),
    (EARTH, "Which of Earth's layers is at the very center of the planet?", "The core",
     ["The crust", "The mantle", "The atmosphere"],
     "The core is the innermost layer, made mostly of iron and nickel.", "medium"),
    (FORCE, "Sound travels through the air as", "vibrations", ["light waves", "heat", "electricity"],
     "Sound is caused by vibrations that travel through air (or another material) to our ears.", "medium"),
    (FORCE, "Why can't sound travel through empty space (a vacuum)?", "Sound needs a material like air or water to travel through",
     ["Sound is too fast for space", "Space is too cold for sound", "Sound only travels through metal"],
     "Sound is a vibration that needs particles of matter (like air) to move through — there are none in a vacuum.", "hard"),
    (FORCE, "What happens to the pitch of a sound when something vibrates faster?", "The pitch gets higher",
     ["The pitch gets lower", "The volume gets louder", "The sound disappears"],
     "Faster vibrations produce a higher pitch; slower vibrations produce a lower pitch.", "hard"),
    (FORCE, "Light bounces off a mirror in a process called", "reflection", ["refraction", "absorption", "conduction"],
     "Reflection is when light bounces off a surface, like a mirror.", "medium"),
    (FORCE, "What force acts against a rolling ball and eventually slows it down on the ground?", "Friction",
     ["Gravity", "Magnetism", "Inertia"],
     "Friction is a force between two surfaces in contact that resists motion.", "easy"),
    (MATTER, "What is matter?", "Anything that has mass and takes up space",
     ["Only things that are alive", "Only solids and liquids", "Anything that produces light"],
     "Matter is defined as anything that has mass and takes up space (volume).", "medium"),
    (MATTER, "Which property of matter is measured in grams or kilograms?", "Mass",
     ["Volume", "Temperature", "Length"],
     "Mass, the amount of matter in an object, is commonly measured in grams or kilograms.", "medium"),
    (MATTER, "Which property of matter is measured in milliliters or liters?", "Volume",
     ["Mass", "Temperature", "Weight"],
     "Volume, the amount of space matter takes up, is measured in milliliters or liters (for liquids).", "medium"),
    (ORGANISMS, "In a food chain, where does the energy that living things need ultimately come from?", "The Sun",
     ["The soil", "The air", "Water"],
     "Nearly all food chains begin with energy from the Sun, captured by producers like plants.", "medium"),
    (ORGANISMS, "What is a habitat?", "The natural environment where an organism lives and can meet its needs",
     ["A type of food an animal eats", "A group of different species", "A tool scientists use to observe animals"],
     "A habitat is the place an organism naturally lives, providing food, water, shelter, and space.", "medium"),
    (ORGANISMS, "A group of the same kind of organism living together in one area is called a", "population",
     ["community", "ecosystem", "habitat"],
     "A population is all the members of one species living in the same area.", "hard"),
    (ORGANISMS, "An ecosystem includes", "both living things and the nonliving environment they interact with",
     ["only the plants in an area", "only the animals in an area", "only the weather in an area"],
     "An ecosystem is made up of living organisms interacting with each other and with nonliving parts of their environment, like water, air, and soil.", "hard"),
    (INVESTIGATION, "What is usually the first step of a scientific investigation?", "Asking a testable question",
     ["Publishing the results", "Forming a final conclusion", "Buying lab equipment"],
     "Scientific investigations typically begin with a question based on an observation.", "easy"),
    (INVESTIGATION, "Why do scientists repeat an experiment several times?", "To make sure the results are reliable and not just a coincidence",
     ["To use up their materials", "Because the first result is always wrong", "To make the experiment take longer"],
     "Repeating trials helps scientists confirm their results are consistent and trustworthy.", "hard"),
    (INVESTIGATION, "Which tool would be best for observing very small details on an insect?", "A hand lens or microscope",
     ["A thermometer", "A balance", "A stopwatch"],
     "A hand lens or microscope magnifies small details that are hard to see with just your eyes.", "easy"),
    (INVESTIGATION, "A prediction about what will happen in an experiment, based on prior knowledge, is called a", "hypothesis",
     ["conclusion", "variable", "observation"],
     "A hypothesis is an educated guess or prediction that can be tested.", "medium"),
    (MATTER, "Which safety practice is most important when handling chemicals in a science experiment?", "Wearing safety goggles and following the teacher's instructions",
     ["Tasting the chemicals to identify them", "Mixing chemicals together to see what happens", "Working without adult supervision"],
     "Safety goggles and following instructions protect against accidental spills or splashes.", "easy"),
]


def _example_of_questions(rng, target):
    out = []
    seen = set()
    for group_key, (topic, base_difficulty, categories) in CATEGORY_GROUPS.items():
        cat_names = list(categories.keys())
        for cat, items in categories.items():
            other_items = [(c, it) for c in cat_names if c != cat for it in categories[c]]
            for item in items:
                key = ("ex", group_key, cat, item)
                if key in seen:
                    continue
                seen.add(key)
                distractors = [it for _, it in rng.sample(other_items, min(3, len(other_items)))]
                if len(distractors) < 3:
                    continue
                qtext = f"Which of these is {cat}?"
                correct = item.capitalize() if item[0].islower() else item
                choices_correct = item[0].upper() + item[1:]
                distractors_cap = [d[0].upper() + d[1:] for d in distractors]
                explanation = f"{choices_correct} is {cat}."
                out.append(make_question(SUBJECT, topic, qtext, choices_correct, distractors_cap, explanation, base_difficulty, rng))
    rng.shuffle(out)
    return out[:target] if target else out


def _not_example_of_questions(rng, target):
    out = []
    seen = set()
    for group_key, (topic, _base_difficulty, categories) in CATEGORY_GROUPS.items():
        cat_names = list(categories.keys())
        if len(cat_names) < 2:
            continue
        for cat, items in categories.items():
            if len(items) < 3:
                continue
            other_items = [(c, it) for c in cat_names if c != cat for it in categories[c]]
            if not other_items:
                continue
            combos = min(len(items), 6)
            for correct_items in [rng.sample(items, min(3, len(items))) for _ in range(combos)]:
                if len(correct_items) < 3:
                    continue
                wrong_cat, wrong_item = rng.choice(other_items)
                key = ("notex", group_key, cat, tuple(sorted(correct_items)), wrong_item)
                if key in seen:
                    continue
                seen.add(key)
                choices = [c[0].upper() + c[1:] for c in correct_items]
                wrong_choice = wrong_item[0].upper() + wrong_item[1:]
                qtext = f"Which of these is NOT {cat}?"
                explanation = f"{wrong_choice} is {wrong_cat} instead — the other three are {cat}."
                out.append(make_question(SUBJECT, topic, qtext, wrong_choice, choices, explanation, "hard", rng))
    rng.shuffle(out)
    return out[:target] if target else out


def _definition_questions(rng, target):
    out = []
    seen = set()
    for cluster_key, (topic, difficulty, terms) in TERM_CLUSTERS.items():
        term_names = list(terms.keys())
        for term, definition in terms.items():
            key = ("def", cluster_key, term)
            if key in seen:
                continue
            seen.add(key)
            others = [t for t in term_names if t != term]
            distractors = rng.sample(others, min(3, len(others)))
            if len(distractors) < 3:
                continue
            qtext = f"What is the term for {definition}?"
            explanation = f"{term} means {definition[0].lower()}{definition[1:]}."
            out.append(make_question(SUBJECT, topic, qtext, term, distractors, explanation, difficulty, rng))

            qtext2 = f"What does '{term}' mean?"
            def_distractors = [terms[t] for t in distractors]
            explanation2 = f"{term} is defined as: {definition}."
            out.append(make_question(SUBJECT, topic, qtext2, definition.capitalize(), [d.capitalize() for d in def_distractors], explanation2, difficulty, rng))
    rng.shuffle(out)
    return out[:target] if target else out


def _sequence_questions(rng, target):
    out = []
    seen = set()
    for seq_key, (topic, stages, label) in SEQUENCES.items():
        n = len(stages)
        for i, stage in enumerate(stages):
            # next stage
            if i < n - 1:
                key = ("next", seq_key, i)
                if key not in seen:
                    seen.add(key)
                    correct = stages[i + 1]
                    distractors = [s for j, s in enumerate(stages) if j != i + 1]
                    difficulty = "easy" if i == 0 else "medium"
                    qtext = f"In the {label}, what stage comes right after '{stage}'?"
                    explanation = f"The order of the {label} is: {' -> '.join(stages)}."
                    out.append(make_question(SUBJECT, topic, qtext, correct, distractors[:3], explanation, difficulty, rng))
            # previous stage
            if i > 0:
                key = ("prev", seq_key, i)
                if key not in seen:
                    seen.add(key)
                    correct = stages[i - 1]
                    distractors = [s for j, s in enumerate(stages) if j != i - 1]
                    difficulty = "medium"
                    qtext = f"In the {label}, what stage comes right before '{stage}'?"
                    explanation = f"The order of the {label} is: {' -> '.join(stages)}."
                    out.append(make_question(SUBJECT, topic, qtext, correct, distractors[:3], explanation, difficulty, rng))
        # first / last
        key = ("first", seq_key)
        if key not in seen:
            seen.add(key)
            qtext = f"Which is the very first stage of the {label}?"
            distractors = stages[1:4] if len(stages) >= 4 else stages[1:]
            out.append(make_question(SUBJECT, topic, qtext, stages[0], distractors[:3], f"The {label} begins with: {stages[0]}.", "easy", rng))
        key = ("last", seq_key)
        if key not in seen:
            seen.add(key)
            qtext = f"Which is the last stage of the {label} (before it starts again or finishes)?"
            distractors = stages[:-1][-3:]
            out.append(make_question(SUBJECT, topic, qtext, stages[-1], distractors[:3], f"The {label} ends with: {stages[-1]}.", "easy", rng))
        # skip-ahead ("hard") — two steps after
        for i in range(n - 2):
            key = ("skip", seq_key, i)
            if key in seen:
                continue
            seen.add(key)
            correct = stages[i + 2]
            distractors = [s for j, s in enumerate(stages) if j != i + 2]
            qtext = f"In the {label}, which stage comes two steps after '{stages[i]}'?"
            explanation = f"The order of the {label} is: {' -> '.join(stages)}."
            out.append(make_question(SUBJECT, topic, qtext, correct, distractors[:3], explanation, "hard", rng))

    rng.shuffle(out)
    return out[:target] if target else out


def _direct_fact_questions(rng):
    out = []
    for topic, qtext, correct, distractors, explanation, difficulty in DIRECT_FACTS:
        out.append(make_question(SUBJECT, topic, qtext, correct, distractors, explanation, difficulty, rng))
    return out


def generate_science_questions(total=300, easy_ratio=0.2, medium_ratio=0.5, hard_ratio=0.3):
    rng = random.Random(SEED)
    pool = []
    pool += _example_of_questions(rng, None)
    pool += _not_example_of_questions(rng, None)
    pool += _definition_questions(rng, None)
    pool += _sequence_questions(rng, None)
    pool += _direct_fact_questions(rng)

    easy_n = round(total * easy_ratio)
    medium_n = round(total * medium_ratio)
    hard_n = total - easy_n - medium_n
    return select_balanced(pool, easy_n, medium_n, hard_n, rng)


if __name__ == "__main__":
    from collections import Counter
    qs = generate_science_questions()
    print("total:", len(qs))
    print("by difficulty:", Counter(q["difficulty"] for q in qs))
    print("by topic:", Counter(q["topic"] for q in qs))
    for q in qs[:10]:
        print("-", q["question_text"], "=>", q["correct_choice"], q[f"choice_{q['correct_choice'].lower()}"])
