"""
Starter question bank for the 5th Grade TEKS Quiz app.

Content is organized by subject -> topic, with topics labeled after the
Texas Essential Knowledge and Skills (TEKS) strands for Grade 5. TEKS codes
shown are strand-level references for organizing content; always verify
exact standard text against the official TEA TEKS documents at
https://tea.texas.gov when using this for formal instruction.
"""

SUBJECTS = [
    {"slug": "math", "name": "Math", "color": "#3B82F6", "icon": "🔢"},
    {"slug": "science", "name": "Science", "color": "#22C55E", "icon": "🔬"},
    {"slug": "english", "name": "English", "color": "#F59E0B", "icon": "📚"},
]

TOPICS = {
    "math": [
        ("Number & Operations", "TEKS 5.3"),
        ("Algebraic Reasoning", "TEKS 5.4"),
        ("Geometry & Measurement", "TEKS 5.5-5.6"),
        ("Data Analysis", "TEKS 5.9"),
        ("Personal Financial Literacy", "TEKS 5.10"),
    ],
    "science": [
        ("Matter and Energy", "TEKS 5.5"),
        ("Force, Motion, and Energy", "TEKS 5.6"),
        ("Earth and Space", "TEKS 5.7-5.8"),
        ("Organisms and Environments", "TEKS 5.9-5.10"),
        ("Scientific Investigation", "TEKS 5.2-5.4"),
    ],
    "english": [
        ("Vocabulary", "TEKS ELAR.5.2"),
        ("Grammar & Conventions", "TEKS ELAR.5.11"),
        ("Reading Comprehension", "TEKS ELAR.5.6"),
        ("Literary Elements", "TEKS ELAR.5.8"),
        ("Writing & Composition", "TEKS ELAR.5.11"),
    ],
}

# Each question: subject, topic, question, choices A-D, correct letter, explanation, difficulty
QUESTIONS = [
    # ---------------- MATH ----------------
    ("math", "Number & Operations", "Round 4,827 to the nearest hundred.",
     "4,800", "4,830", "4,900", "5,000", "A",
     "4,827 is between 4,800 and 4,900. Since 27 is less than 50, round down to 4,800.", "easy"),
    ("math", "Number & Operations", "What is 3/4 + 1/8?",
     "4/12", "7/8", "1/2", "5/8", "B",
     "3/4 = 6/8, and 6/8 + 1/8 = 7/8.", "medium"),
    ("math", "Number & Operations", "What is 2.35 + 1.7?",
     "2.52", "3.42", "4.05", "4.55", "C",
     "Line up the decimal points: 2.35 + 1.70 = 4.05.", "medium"),
    ("math", "Number & Operations", "What is 0.6 x 0.3?",
     "0.18", "1.8", "0.9", "0.018", "A",
     "6 x 3 = 18, and there are 2 total decimal places, so 0.6 x 0.3 = 0.18.", "hard"),
    ("math", "Number & Operations", "What is 456 divided by 8?",
     "55", "57", "56", "58", "B",
     "8 x 57 = 456.", "medium"),
    ("math", "Number & Operations", "Which fraction is equivalent to 2/3?",
     "4/9", "6/9", "3/6", "5/6", "B",
     "Multiply the numerator and denominator by 3: 2/3 = 6/9.", "easy"),
    ("math", "Algebraic Reasoning", "What is the value of 3 x (4 + 2)?",
     "14", "18", "20", "9", "B",
     "First solve inside the parentheses: 4 + 2 = 6, then 3 x 6 = 18.", "easy"),
    ("math", "Algebraic Reasoning", "What is the value of n if n + 15 = 32?",
     "16", "17", "18", "47", "B",
     "Subtract 15 from both sides: 32 - 15 = 17.", "easy"),
    ("math", "Algebraic Reasoning", "Which number pattern follows the rule 'add 6'?",
     "2, 8, 14, 20", "2, 8, 16, 24", "2, 10, 18, 26", "2, 6, 12, 18", "A",
     "Each number increases by exactly 6: 2, 2+6=8, 8+6=14, 14+6=20.", "medium"),
    ("math", "Geometry & Measurement", "How many faces does a rectangular prism have?",
     "4", "6", "8", "12", "B",
     "A rectangular prism (like a box) has 6 flat faces.", "easy"),
    ("math", "Geometry & Measurement", "What is the area of a rectangle with length 8 cm and width 5 cm?",
     "13 cm²", "26 cm²", "40 cm²", "45 cm²", "C",
     "Area = length x width = 8 x 5 = 40 cm².", "medium"),
    ("math", "Geometry & Measurement", "What is the volume of a cube with a side length of 3 cm?",
     "9 cm³", "27 cm³", "18 cm³", "6 cm³", "B",
     "Volume = length x width x height = 3 x 3 x 3 = 27 cm³.", "hard"),
    ("math", "Geometry & Measurement", "On a coordinate grid, what is the x-coordinate of the point (3, 5)?",
     "3", "5", "8", "15", "A",
     "In an ordered pair (x, y), the first number is always the x-coordinate.", "easy"),
    ("math", "Geometry & Measurement", "What is the perimeter of a square with a side length of 7 inches?",
     "14 in", "21 in", "28 in", "49 in", "C",
     "Perimeter of a square = 4 x side = 4 x 7 = 28 inches.", "medium"),
    ("math", "Data Analysis", "In the data set 4, 7, 7, 9, 3, what is the mode?",
     "3", "4", "7", "9", "C",
     "The mode is the number that appears most often. 7 appears twice.", "easy"),
    ("math", "Data Analysis", "What is the mean of the data set 2, 4, 6, 8, 10?",
     "5", "6", "7", "8", "B",
     "Add all numbers (2+4+6+8+10=30) and divide by how many there are (5): 30 / 5 = 6.", "medium"),
    ("math", "Personal Financial Literacy", "An item costs $12.50. You pay with a $20 bill. How much change should you get?",
     "$6.50", "$7.00", "$7.50", "$8.00", "C",
     "$20.00 - $12.50 = $7.50.", "easy"),
    ("math", "Personal Financial Literacy", "Which is the best way to grow your savings over time?",
     "Spend it all right away", "Put it in a savings account that earns interest",
     "Hide the cash under a mattress", "Lend it out with no plan to be repaid", "B",
     "A savings account earns interest, meaning your money grows over time just by saving it.", "medium"),

    # ---------------- SCIENCE ----------------
    ("science", "Matter and Energy", "What happens when water changes from a liquid to a gas?",
     "Freezing", "Melting", "Evaporation", "Condensation", "C",
     "Evaporation is the process where liquid water turns into water vapor (a gas).", "easy"),
    ("science", "Matter and Energy", "Which of these is an example of a physical change?",
     "Burning wood", "Rusting iron", "Melting ice", "Baking a cake", "C",
     "Melting ice changes its state (solid to liquid) but it's still water — no new substance is formed.", "medium"),
    ("science", "Matter and Energy", "Matter that has a definite shape and a definite volume is a",
     "Liquid", "Gas", "Solid", "Plasma", "C",
     "Solids keep their own shape and volume, unlike liquids and gases.", "easy"),
    ("science", "Matter and Energy", "Mixing sand and water together creates a",
     "Solution", "New substance", "Mixture", "Compound", "C",
     "Sand and water can be physically separated again, so together they form a mixture.", "medium"),
    ("science", "Force, Motion, and Energy", "Which of these is a form of energy?",
     "Rock", "Sound", "Table", "Chair", "B",
     "Sound is energy that travels in waves; a rock, table, and chair are objects made of matter.", "easy"),
    ("science", "Force, Motion, and Energy", "A push or a pull on an object is called a",
     "Motion", "Force", "Speed", "Mass", "B",
     "A force is any push or pull that can change an object's motion.", "easy"),
    ("science", "Force, Motion, and Energy", "Which best describes potential energy?",
     "Energy of motion", "Stored energy", "Energy that is destroyed", "Sound energy", "B",
     "Potential energy is stored energy, like a ball held up high before it's dropped.", "hard"),
    ("science", "Force, Motion, and Energy", "Light travels in",
     "Curves", "Straight lines", "Circles", "Zigzags", "B",
     "Light travels in straight lines until it hits something that reflects, bends, or blocks it.", "medium"),
    ("science", "Earth and Space", "What causes day and night on Earth?",
     "Earth's revolution around the sun", "Earth's rotation on its axis",
     "The moon's orbit around Earth", "Earth's tilt alone", "B",
     "Earth spins (rotates) on its axis once about every 24 hours, causing day and night.", "medium"),
    ("science", "Earth and Space", "Which of these is a renewable resource?",
     "Coal", "Oil", "Wind", "Natural gas", "C",
     "Wind is naturally replenished and will not run out, unlike fossil fuels such as coal, oil, and natural gas.", "easy"),
    ("science", "Earth and Space", "Weathering and erosion mainly change Earth's",
     "Core", "Surface", "Atmosphere", "Magnetic field", "B",
     "Weathering breaks down rock and erosion moves it, both reshaping Earth's surface over time.", "medium"),
    ("science", "Earth and Space", "Which layer of Earth do people live on?",
     "Core", "Mantle", "Crust", "Atmosphere", "C",
     "The crust is Earth's thin, outermost solid layer where we live.", "easy"),
    ("science", "Organisms and Environments", "A food chain almost always begins with",
     "A decomposer", "A producer", "A predator", "A consumer", "B",
     "Producers, like plants, make their own food from sunlight and start most food chains.", "medium"),
    ("science", "Organisms and Environments", "Which of these is an example of a decomposer?",
     "Oak tree", "Rabbit", "Mushroom", "Hawk", "C",
     "Mushrooms (fungi) break down dead plants and animals, returning nutrients to the soil.", "medium"),
    ("science", "Organisms and Environments", "Which adaptation would help an animal survive in the desert?",
     "Thick fur", "Storing fat to use for water", "Living in ice", "Breathing underwater", "B",
     "Some desert animals, like camels, store fat that can be used for energy and water when both are scarce.", "hard"),
    ("science", "Organisms and Environments", "In an ecosystem, energy generally flows from",
     "Consumers to producers", "Producers to consumers", "Decomposers to producers only", "It does not flow", "B",
     "Producers capture energy from the sun, and that energy passes to consumers that eat them.", "medium"),
    ("science", "Scientific Investigation", "Which tool is best for measuring the mass of an object?",
     "Ruler", "Thermometer", "Balance or scale", "Beaker", "C",
     "A balance or scale measures mass; rulers measure length, thermometers measure temperature, and beakers measure volume.", "easy"),
    ("science", "Scientific Investigation", "What is usually the first step in a scientific investigation?",
     "Form a conclusion", "Ask a question", "Publish the results", "Skip making observations", "B",
     "Scientific investigations typically start by asking a testable question based on an observation.", "easy"),

    # ---------------- ENGLISH ----------------
    ("english", "Vocabulary", "Choose the synonym for 'enormous.'",
     "Tiny", "Huge", "Fast", "Quiet", "B",
     "A synonym is a word with a similar meaning. 'Huge' means about the same as 'enormous.'", "easy"),
    ("english", "Vocabulary", "Choose the antonym for 'generous.'",
     "Kind", "Selfish", "Wealthy", "Happy", "B",
     "An antonym is a word with the opposite meaning. 'Selfish' is the opposite of 'generous.'", "easy"),
    ("english", "Vocabulary", "What does the prefix 'un-' mean in the word 'unhappy'?",
     "Again", "Not", "Before", "Under", "B",
     "The prefix 'un-' means 'not,' so 'unhappy' means 'not happy.'", "medium"),
    ("english", "Vocabulary", "What does the suffix '-ful' mean in the word 'joyful'?",
     "Without", "Full of", "Before", "Small", "B",
     "The suffix '-ful' means 'full of,' so 'joyful' means 'full of joy.'", "medium"),
    ("english", "Grammar & Conventions", "Which sentence is punctuated correctly?",
     "\"Lets go to the park.\"", "\"Let's go to the park.\"",
     "\"Lets, go to the park.\"", "\"Lets go, to the park.\"", "B",
     "The contraction 'let's' (let us) needs an apostrophe: Let's.", "easy"),
    ("english", "Grammar & Conventions", "Which word is the verb in the sentence 'The dog barked loudly'?",
     "Dog", "Barked", "Loudly", "The", "B",
     "'Barked' shows the action the dog did, making it the verb.", "easy"),
    ("english", "Grammar & Conventions", "Which sentence has correct subject-verb agreement?",
     "\"The boys is playing.\"", "\"The boys are playing.\"",
     "\"The boys am playing.\"", "\"The boys be playing.\"", "B",
     "'Boys' is plural, so it needs the plural verb 'are,' not 'is,' 'am,' or 'be.'", "medium"),
    ("english", "Grammar & Conventions", "Which sentence correctly shows a plural possessive noun?",
     "\"The dogs' bones\" (for many dogs)", "\"The dog's's bones\"",
     "\"The dogs bones'\"", "\"Dogs' the bones\"", "A",
     "For a plural noun already ending in s, add just an apostrophe: dogs'.", "hard"),
    ("english", "Reading Comprehension", "The main idea of a passage is",
     "A small, unimportant detail", "The central point the author wants you to understand",
     "Only the last sentence", "A character's name", "B",
     "The main idea is the most important point the whole passage is about.", "easy"),
    ("english", "Reading Comprehension", "When you predict what will happen next in a story, you are using",
     "Context clues", "Prior knowledge and details from the text", "The glossary", "The table of contents", "B",
     "Predicting means using clues in the text plus what you already know to guess what happens next.", "medium"),
    ("english", "Reading Comprehension", "Figuring out a word's meaning by looking at the words around it is called",
     "Skimming", "Using context clues", "Summarizing", "Making an inference", "B",
     "Context clues are hints from surrounding words and sentences that help explain an unfamiliar word.", "medium"),
    ("english", "Reading Comprehension", "A story's setting refers to",
     "The characters' feelings", "The time and place the story happens",
     "The problem in the story", "The lesson learned", "B",
     "Setting tells the reader when and where the events of the story take place.", "easy"),
    ("english", "Literary Elements", "The lesson or message of a story is called the",
     "Plot", "Theme", "Setting", "Climax", "B",
     "The theme is the underlying message or lesson the author wants readers to take away.", "medium"),
    ("english", "Literary Elements", "\"The wind whispered through the trees\" is an example of",
     "Simile", "Personification", "Metaphor", "Hyperbole", "B",
     "Personification gives human qualities, like whispering, to something that isn't human.", "medium"),
    ("english", "Literary Elements", "A comparison using the words 'like' or 'as' is called",
     "A metaphor", "A simile", "Personification", "Alliteration", "B",
     "A simile compares two different things using 'like' or 'as,' such as 'brave as a lion.'", "easy"),
    ("english", "Writing & Composition", "Which is the best topic sentence for a paragraph about recycling?",
     "\"I like pizza.\"", "\"Recycling helps protect our planet in many ways.\"",
     "\"Yesterday was sunny.\"", "\"My dog is brown.\"", "B",
     "A topic sentence should introduce the main idea of the paragraph — here, that's recycling and the planet.", "easy"),
    ("english", "Writing & Composition", "What should a writer focus on during the revising stage?",
     "Publishing the final copy", "Improving ideas, organization, and word choice",
     "Checking spelling only", "Choosing a topic", "B",
     "Revising is about making the writing better — stronger ideas, clearer organization, and better word choice — before final edits.", "hard"),
    ("english", "Writing & Composition", "Which of these is a complete sentence?",
     "\"Running to the store.\"", "\"Because it was raining.\"",
     "\"She ran to the store.\"", "\"The big red.\"", "C",
     "A complete sentence needs a subject and a verb that express a full thought: 'She ran to the store.'", "medium"),
]

# Questions that display a diagram/chart image above the answer choices.
# image_path is relative to the app's static/ folder.
DIAGRAM_QUESTIONS = [
    {
        "subject": "science", "topic": "Organisms and Environments",
        "question_text": "Look at the butterfly life cycle diagram. Which stage comes right after the Larva (caterpillar) stage?",
        "choice_a": "Egg", "choice_b": "Pupa (Chrysalis)", "choice_c": "Adult Butterfly", "choice_d": "Larva again",
        "correct_choice": "B",
        "explanation": "The order is Egg -> Larva -> Pupa -> Adult. Inside the pupa (chrysalis), the caterpillar changes into a butterfly.",
        "difficulty": "easy",
        "image_path": "img/diagrams/butterfly_life_cycle.svg",
    },
    {
        "subject": "science", "topic": "Earth and Space",
        "question_text": "In the water cycle diagram, what process is happening at Label A, where water rises from the ocean toward the clouds?",
        "choice_a": "Precipitation", "choice_b": "Condensation", "choice_c": "Evaporation", "choice_d": "Collection",
        "correct_choice": "C",
        "explanation": "Evaporation happens when the sun heats water and turns it into water vapor, which rises into the air.",
        "difficulty": "medium",
        "image_path": "img/diagrams/water_cycle.svg",
    },
    {
        "subject": "science", "topic": "Organisms and Environments",
        "question_text": "Look at the plant diagram. Which labeled part's main job is to absorb water and nutrients from the soil?",
        "choice_a": "1 - Roots", "choice_b": "2 - Stem", "choice_c": "3 - Leaves", "choice_d": "4 - Flower",
        "correct_choice": "A",
        "explanation": "Roots grow underground and absorb water and nutrients, then the stem carries them up to the rest of the plant.",
        "difficulty": "easy",
        "image_path": "img/diagrams/plant_parts.svg",
    },
    {
        "subject": "math", "topic": "Data Analysis",
        "question_text": "According to the bar graph, how many more students chose Apples than Grapes as their favorite fruit?",
        "choice_a": "3", "choice_b": "5", "choice_c": "8", "choice_d": "11",
        "correct_choice": "B",
        "explanation": "Apples got 8 votes and Grapes got 3 votes. 8 - 3 = 5 more students chose Apples.",
        "difficulty": "medium",
        "image_path": "img/diagrams/bar_graph_fruit.svg",
    },
    {
        "subject": "math", "topic": "Geometry & Measurement",
        "question_text": "Using the diagram of the garden plot, what is the area of the rectangle?",
        "choice_a": "13 cm²", "choice_b": "26 cm²", "choice_c": "36 cm²", "choice_d": "40 cm²",
        "correct_choice": "C",
        "explanation": "Area = length x width = 9 cm x 4 cm = 36 cm².",
        "difficulty": "medium",
        "image_path": "img/diagrams/rectangle_dimensions.svg",
    },
    {
        "subject": "english", "topic": "Literary Elements",
        "question_text": "Look at the story mountain (plot diagram). Which part of the plot is labeled at the very top of the mountain?",
        "choice_a": "Exposition", "choice_b": "Rising Action", "choice_c": "Climax", "choice_d": "Resolution",
        "correct_choice": "C",
        "explanation": "The climax is the most exciting, turning-point moment of the story, shown at the peak of the story mountain.",
        "difficulty": "medium",
        "image_path": "img/diagrams/plot_diagram.svg",
    },
]


def seed_database(db):
    """Insert subjects, topics, and starter questions. Safe to call on an empty DB."""
    subject_ids = {}
    for s in SUBJECTS:
        cur = db.execute(
            "INSERT OR IGNORE INTO subjects (slug, name, color, icon) VALUES (?, ?, ?, ?)",
            (s["slug"], s["name"], s["color"], s["icon"]),
        )
        row = db.execute("SELECT id FROM subjects WHERE slug = ?", (s["slug"],)).fetchone()
        subject_ids[s["slug"]] = row["id"]

    topic_ids = {}
    for subject_slug, topics in TOPICS.items():
        for name, teks_strand in topics:
            db.execute(
                "INSERT INTO topics (subject_id, name, teks_strand) VALUES (?, ?, ?)",
                (subject_ids[subject_slug], name, teks_strand),
            )
            row = db.execute(
                "SELECT id FROM topics WHERE subject_id = ? AND name = ?",
                (subject_ids[subject_slug], name),
            ).fetchone()
            topic_ids[(subject_slug, name)] = row["id"]

    for (subject_slug, topic_name, question_text, a, b, c, d, correct, explanation, difficulty) in QUESTIONS:
        db.execute(
            """INSERT INTO questions
               (subject_id, topic_id, question_text, choice_a, choice_b, choice_c, choice_d,
                correct_choice, explanation, difficulty, image_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
            (
                subject_ids[subject_slug],
                topic_ids[(subject_slug, topic_name)],
                question_text, a, b, c, d, correct, explanation, difficulty,
            ),
        )

    from app.generators.math_gen import generate_math_questions
    from app.generators.science_gen import generate_science_questions
    from app.generators.english_gen import generate_english_questions

    generated = (
        DIAGRAM_QUESTIONS
        + generate_math_questions()
        + generate_science_questions()
        + generate_english_questions()
    )
    for q in generated:
        db.execute(
            """INSERT INTO questions
               (subject_id, topic_id, question_text, choice_a, choice_b, choice_c, choice_d,
                correct_choice, explanation, difficulty, image_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                subject_ids[q["subject"]],
                topic_ids[(q["subject"], q["topic"])],
                q["question_text"], q["choice_a"], q["choice_b"], q["choice_c"], q["choice_d"],
                q["correct_choice"], q["explanation"], q["difficulty"], q["image_path"],
            ),
        )

    db.commit()
