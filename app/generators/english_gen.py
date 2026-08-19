"""Generates a large pool of TEKS Grade 5 English/ELAR questions, then selects
~300 skewed toward medium/tricky difficulty.

Vocabulary and grammar questions are template-generated from curated word
banks and sentence templates (so wording stays natural and correctness is
controlled directly). Reading comprehension includes real short passages
(passages can't be templated the way arithmetic or word lists can) with
questions written specifically against each one.
"""
import random

from app.generators.common import make_question, select_balanced, fill_distractors

SEED = 20260819
SUBJECT = "english"

VOCAB = "Vocabulary"
GRAMMAR = "Grammar & Conventions"
READING = "Reading Comprehension"
LITERARY = "Literary Elements"
WRITING = "Writing & Composition"

# =============================================================== Vocabulary

# (word, synonym, antonym_or_None)
WORD_BANK = [
    ("enormous", "huge", "tiny"), ("generous", "giving", "selfish"), ("courageous", "brave", "cowardly"),
    ("ancient", "very old", "modern"), ("brilliant", "very smart", "dull"), ("exhausted", "very tired", "energetic"),
    ("delicate", "fragile", "sturdy"), ("furious", "very angry", "calm"), ("peculiar", "strange", "ordinary"),
    ("vivid", "brightly colored", "dull"), ("cautious", "careful", "reckless"), ("abundant", "plentiful", "scarce"),
    ("diminish", "to decrease", "to increase"), ("assist", "to help", "to hinder"), ("conceal", "to hide", "to reveal"),
    ("gigantic", "extremely large", "tiny"), ("miserable", "very unhappy", "joyful"), ("frequent", "happening often", "rare"),
    ("genuine", "real", "fake"), ("hostile", "unfriendly", "friendly"), ("timid", "shy", "bold"),
    ("absurd", "ridiculous", "sensible"), ("permit", "to allow", "to forbid"), ("expand", "to grow larger", "to shrink"),
    ("humble", "not boastful", "arrogant"), ("cease", "to stop", "to continue"), ("fragile", "easily broken", "durable"),
    ("triumph", "a great victory", "a defeat"), ("reluctant", "unwilling", "eager"), ("clumsy", "awkward", "graceful"),
    ("drowsy", "sleepy", "alert"), ("astonish", "to amaze", "to bore"), ("gloomy", "dark and sad", "cheerful"),
    ("nimble", "quick and light", "clumsy"), ("stubborn", "unwilling to change one's mind", "flexible"),
    ("vast", "extremely large in area", "tiny"), ("weary", "very tired", "energetic"), ("bizarre", "very strange", "normal"),
    ("swift", "very fast", "slow"), ("faint", "weak or dim", "strong"), ("mend", "to repair", "to break"),
    ("sturdy", "strong and well-built", "flimsy"), ("cramped", "very tight and crowded", "spacious"),
    ("dismal", "gloomy and depressing", "cheerful"), ("elated", "very happy", "miserable"), ("frail", "weak", "sturdy"),
    ("hasty", "done quickly, without care", "careful"), ("immense", "huge", "tiny"), ("jubilant", "joyfully happy", "gloomy"),
    ("lively", "full of energy", "sluggish"), ("modest", "not boastful about oneself", "boastful"),
    ("notorious", "famous for something bad", None), ("obstinate", "stubborn", "flexible"), ("plentiful", "in large amounts", "scarce"),
    ("quaint", "charmingly old-fashioned", None), ("rigid", "stiff, not bending", "flexible"), ("solitary", "alone", None),
    ("tedious", "long and boring", "exciting"), ("unruly", "hard to control", "obedient"), ("vibrant", "full of life and color", "dull"),
    ("wary", "cautious of danger", "trusting"), ("yearn", "to long for something", None), ("zealous", "very enthusiastic", "indifferent"),
    ("ample", "more than enough", "insufficient"), ("blunder", "a careless mistake", None), ("candid", "honest and direct", "deceptive"),
    ("deceive", "to trick someone", None), ("eager", "very excited to do something", "reluctant"), ("feeble", "very weak", "strong"),
    ("gracious", "polite and kind", "rude"), ("hinder", "to get in the way of", "to help"), ("ignite", "to set on fire", "to extinguish"),
    ("jovial", "cheerful and friendly", "gloomy"), ("keen", "very interested or sharp", None), ("lament", "to express sadness about", None),
    ("melancholy", "a feeling of sadness", "joy"), ("nurture", "to care for and help grow", "to neglect"),
    ("optimistic", "expecting good things", "pessimistic"), ("plummet", "to fall suddenly", "to rise"),
    ("resilient", "able to recover quickly", None), ("sluggish", "slow-moving", "swift"), ("thorough", "complete and detailed", "careless"),
    ("unanimous", "in complete agreement", None), ("valiant", "very brave", "cowardly"), ("wilt", "to droop or weaken", None),
]

# A broad pool of common grade-level words used as neutral distractors for vocabulary MC questions.
DISTRACTOR_POOL = [
    "happy", "quick", "loud", "quiet", "friendly", "colorful", "simple", "narrow", "wide", "smooth",
    "rough", "shiny", "curious", "polite", "clever", "gentle", "clumsy", "cheerful", "patient", "nervous",
    "confident", "graceful", "silent", "playful", "serious", "modern", "distant", "nearby", "fresh", "stale",
    "bold", "faint", "steady", "chilly", "warm", "damp", "dry", "sturdy", "flimsy", "vast",
]


def _vocab_distractors(rng, correct, exclude, n=3):
    pool = [w for w in DISTRACTOR_POOL if w not in exclude and w != correct]
    return rng.sample(pool, n)


def gen_vocab_questions(rng):
    out = []
    for word, syn, ant in WORD_BANK:
        difficulty = "easy" if len(word) <= 6 else ("medium" if len(word) <= 9 else "hard")
        distractors = _vocab_distractors(rng, syn, {word, syn, ant})
        qtext = f"Choose the synonym (word with a similar meaning) for '{word}.'"
        explanation = f"A synonym is a word with a similar meaning. '{syn.capitalize()}' means about the same as '{word}.'"
        out.append(make_question(SUBJECT, VOCAB, qtext, syn.capitalize(), [d.capitalize() for d in distractors], explanation, difficulty, rng))

        if ant:
            distractors = _vocab_distractors(rng, ant, {word, syn, ant})
            qtext = f"Choose the antonym (word with the opposite meaning) for '{word}.'"
            explanation = f"An antonym is a word with the opposite meaning. '{ant.capitalize()}' is the opposite of '{word}.'"
            diff2 = "medium" if difficulty == "easy" else "hard"
            out.append(make_question(SUBJECT, VOCAB, qtext, ant.capitalize(), [d.capitalize() for d in distractors], explanation, diff2, rng))
    return out


AFFIXES = [
    ("un-", "prefix", "not / the opposite of", "unhappy"), ("re-", "prefix", "again", "rewrite"),
    ("pre-", "prefix", "before", "preview"), ("dis-", "prefix", "not / the opposite of", "disagree"),
    ("mis-", "prefix", "wrongly / badly", "misspell"), ("non-", "prefix", "not", "nonfiction"),
    ("over-", "prefix", "too much", "overcook"), ("under-", "prefix", "too little / below", "underline"),
    ("bi-", "prefix", "two", "bicycle"), ("tri-", "prefix", "three", "triangle"),
    ("inter-", "prefix", "between", "interstate"), ("semi-", "prefix", "half / partly", "semicircle"),
    ("-ful", "suffix", "full of", "joyful"), ("-less", "suffix", "without", "fearless"),
    ("-able", "suffix", "able to be", "washable"), ("-er", "suffix", "one who does something", "teacher"),
    ("-ist", "suffix", "one who does or believes something", "artist"), ("-ly", "suffix", "in a certain manner", "quickly"),
    ("-ness", "suffix", "the state of being", "kindness"), ("-ment", "suffix", "the result or act of", "movement"),
    ("-tion", "suffix", "the act or state of", "celebration"),
]


def gen_affix_questions(rng):
    out = []
    for affix, kind, meaning, example in AFFIXES:
        others = [m for a, k, m, e in AFFIXES if m != meaning]
        distractors = rng.sample(others, 3)
        qtext = f"What does the {kind} '{affix}' mean in the word '{example}'?"
        explanation = f"The {kind} '{affix}' means '{meaning},' so '{example}' relates to that meaning."
        out.append(make_question(SUBJECT, VOCAB, qtext, meaning.capitalize(), [d.capitalize() for d in distractors], explanation, "medium", rng))
    return out


# =============================================================== Grammar & Conventions

SUBJECTS_SING = ["The dog", "The teacher", "My sister", "The bird", "The student", "The chef", "The baby",
                  "The cat", "The scientist", "The artist", "The puppy", "Our neighbor"]
SUBJECTS_PLUR = ["The dogs", "The teachers", "My sisters", "The birds", "The students", "The chefs", "The babies",
                  "The cats", "The scientists", "The artists", "The puppies", "Our neighbors"]
VERB_ING_PHRASES = ["playing outside", "singing a song", "reading a book", "painting a picture", "running fast",
                     "jumping rope", "writing a story", "laughing loudly", "cooking dinner", "riding a bike",
                     "building a fort", "watching a movie"]


def gen_subject_verb_agreement(rng, target):
    out = []
    seen = set()
    attempts = 0
    while len(out) < target and attempts < target * 6:
        attempts += 1
        plural = rng.random() < 0.5
        idx = rng.randrange(len(SUBJECTS_SING))
        subject = SUBJECTS_PLUR[idx] if plural else SUBJECTS_SING[idx]
        verb_phrase = rng.choice(VERB_ING_PHRASES)
        key = (subject, verb_phrase)
        if key in seen:
            continue
        seen.add(key)
        correct_be = "are" if plural else "is"
        wrong_bes = [b for b in ["is", "are", "am", "be"] if b != correct_be]
        qtext = f"Which sentence has correct subject-verb agreement?"
        correct_sentence = f'"{subject} {correct_be} {verb_phrase}."'
        distractor_sentences = [f'"{subject} {b} {verb_phrase}."' for b in wrong_bes]
        explanation = (
            f"'{subject}' is {'plural' if plural else 'singular'}, so it needs the "
            f"{'plural' if plural else 'singular'} verb '{correct_be}.'"
        )
        out.append(make_question(SUBJECT, GRAMMAR, qtext, correct_sentence, distractor_sentences, explanation, "medium", rng))
    return out


CONTRACTIONS = [
    ("Let's", "Lets"), ("Don't", "Dont"), ("Can't", "Cant"), ("It's", "Its"), ("They're", "Theyre"),
    ("You're", "Youre"), ("We're", "Were"), ("I'm", "Im"), ("Won't", "Wont"), ("Isn't", "Isnt"),
    ("Doesn't", "Doesnt"), ("Didn't", "Didnt"), ("Wasn't", "Wasnt"), ("Couldn't", "Couldnt"),
    ("Shouldn't", "Shouldnt"), ("Wouldn't", "Wouldnt"), ("Haven't", "Havent"), ("Hasn't", "Hasnt"),
]
CONTEXT_ENDINGS = ["go to the park.", "have a great day.", "see the ocean.", "play the game.",
                    "finish the homework.", "go outside now.", "understand the question.",
                    "forget the address.", "find the keys.", "believe the story."]


def gen_contraction_questions(rng, target):
    out = []
    seen = set()
    attempts = 0
    while len(out) < target and attempts < target * 6:
        attempts += 1
        correct, no_apostrophe = rng.choice(CONTRACTIONS)
        context = rng.choice(CONTEXT_ENDINGS)
        key = (correct, context)
        if key in seen:
            continue
        seen.add(key)
        correct_sentence = f'"{correct} {context}"'
        wrong1 = f'"{no_apostrophe} {context}"'
        wrong2 = f'"{no_apostrophe}\' {context}"'
        wrong3 = f'"{correct.replace(chr(39), chr(39)*2, 1)} {context}"'
        qtext = "Which sentence is punctuated correctly?"
        explanation = f"'{correct}' is the correct contraction, with the apostrophe replacing the missing letters."
        out.append(make_question(SUBJECT, GRAMMAR, qtext, correct_sentence, [wrong1, wrong2, wrong3], explanation, "easy", rng))
    return out


# Hand-authored grammar items (safer than templating for subtler rules).
GRAMMAR_DIRECT = [
    ("Which word is a verb in the sentence 'The dog barked loudly'?", "Barked", ["Dog", "Loudly", "The"],
     "'Barked' shows the action the dog did, making it the verb.", "easy"),
    ("Which word is a noun in the sentence 'The children played in the park'?", "Park", ["Played", "In", "The"],
     "'Park' names a place, making it a noun.", "easy"),
    ("Which word is an adjective in the sentence 'The tall boy ran quickly'?", "Tall", ["Boy", "Ran", "Quickly"],
     "'Tall' describes the noun 'boy,' making it an adjective.", "medium"),
    ("Which word is an adverb in the sentence 'She sang beautifully'?", "Beautifully", ["Sang", "She", "A"],
     "'Beautifully' describes how she sang, making it an adverb.", "medium"),
    ("Which word is a pronoun in the sentence 'He gave her the book'?", "He", ["Book", "Gave", "The"],
     "'He' takes the place of a person's name, making it a pronoun.", "medium"),
    ("Which sentence correctly shows a plural possessive noun (bones belonging to many dogs)?",
     "\"The dogs' bones\"", ["\"The dog's's bones\"", "\"The dogs bones'\"", "\"Dogs' the bones\""],
     "For a plural noun already ending in s, add just an apostrophe: dogs'.", "hard"),
    ("Which sentence correctly shows a singular possessive noun (the toy belonging to one cat)?",
     "\"The cat's toy\"", ["\"The cats' toy\"", "\"The cats toy\"", "\"The cat's' toy\""],
     "For a singular noun, add apostrophe + s: cat's.", "medium"),
    ("Which sentence uses capitalization correctly?", "\"We visited Texas last July.\"",
     ["\"we visited texas last july.\"", "\"We visited texas last July.\"", "\"We Visited Texas Last July.\""],
     "Proper nouns (like Texas and July) and the first word of a sentence should be capitalized — but not every word.", "medium"),
    ("Which sentence uses capitalization correctly?", "\"My teacher, Mr. Lopez, is from Houston.\"",
     ["\"my teacher, mr. Lopez, is from houston.\"", "\"My Teacher, Mr. Lopez, Is From Houston.\"", "\"My teacher, mr. lopez, is from Houston.\""],
     "Names of specific people and places (Mr. Lopez, Houston) are capitalized, but common nouns like 'teacher' are not.", "hard"),
    ("Which is a complete sentence?", "\"She ran to the store.\"",
     ["\"Running to the store.\"", "\"Because it was raining.\"", "\"The big red.\""],
     "A complete sentence needs a subject and a verb that express a full thought.", "medium"),
    ("Which is a complete sentence?", "\"The kids played outside all afternoon.\"",
     ["\"Played outside all afternoon.\"", "\"All afternoon in the yard.\"", "\"Outside, running and laughing.\""],
     "A complete sentence needs both a subject ('the kids') and a verb ('played').", "medium"),
    ("Which sentence is a simple sentence (one independent clause)?", "\"The wind blew all night.\"",
     ["\"The wind blew all night, and the trees swayed.\"", "\"Although it was windy, we went outside.\"", "\"The wind blew, the rain fell, and the sky darkened.\""],
     "A simple sentence has exactly one independent clause with a subject and a verb.", "medium"),
    ("Which sentence is a compound sentence (two independent clauses joined by 'and,' 'but,' or 'or')?",
     "\"I wanted to go outside, but it started raining.\"",
     ["\"I wanted to go outside because it was sunny.\"", "\"Wanting to go outside, I grabbed my coat.\"", "\"I went outside.\""],
     "A compound sentence joins two complete sentences with a comma and a conjunction like 'but.'", "hard"),
    ("Which sentence is a complex sentence (has a dependent clause)?",
     "\"Because it was raining, we stayed inside.\"",
     ["\"It was raining, and we stayed inside.\"", "\"We stayed inside.\"", "\"It rained all day.\""],
     "A complex sentence includes a dependent clause (like 'Because it was raining') that can't stand alone.", "hard"),
    ("Choose the word that correctly completes the sentence: '___ going to the store.'", "\"They're\"",
     ["\"Their\"", "\"There\"", "\"Them\""], "'They're' is the contraction for 'they are.'", "medium"),
    ("Choose the word that correctly completes the sentence: 'The dog wagged ___ tail.'", "\"its\"",
     ["\"it's\"", "\"its'\"", "\"it is\""], "'Its' (no apostrophe) shows possession — the tail belongs to the dog.", "hard"),
    ("Choose the word that correctly completes the sentence: 'Is this ___ backpack?'", "\"your\"",
     ["\"you're\"", "\"yore\"", "\"yours're\""], "'Your' shows possession, meaning 'belonging to you.'", "medium"),
    ("Choose the word that correctly completes the sentence: 'I have ___ books to carry.'", "\"too many\"",
     ["\"to many\"", "\"two many\"", "\"too much\""], "'Too' here means 'excessively,' matching 'too many.'", "medium"),
    ("Choose the word that correctly completes the sentence: 'We drove ___ the store.'", "\"to\"",
     ["\"too\"", "\"two\"", "\"toward, too\""], "'To' shows direction or destination here.", "easy"),
    ("Choose the word that correctly completes the sentence: 'First we ate lunch, and ___ we went to the park.'",
     "\"then\"", ["\"than\"", "\"then,\"", "\"when\""], "'Then' shows what happened next in time.", "medium"),
    ("Choose the word that correctly completes the sentence: 'This cake is better ___ that one.'", "\"than\"",
     ["\"then\"", "\"that\"", "\"they\""], "'Than' is used to compare two things.", "medium"),
    ("Which sentence uses commas correctly?", "\"For the picnic, we packed sandwiches, apples, and lemonade.\"",
     ["\"For the picnic we packed sandwiches apples and lemonade.\"", "\"For the picnic, we packed sandwiches, apples and, lemonade.\"", "\"For, the picnic we packed sandwiches, apples, and lemonade.\""],
     "Commas separate items in a list and follow an introductory phrase like 'For the picnic.'", "hard"),
    ("Which sentence uses quotation marks correctly for dialogue?", "\"'Watch out!' shouted Maria.\"",
     ["\"Watch out! shouted Maria.\"", "\"'Watch out! shouted Maria.'\"", "\"Watch out!' shouted Maria.\""],
     "Quotation marks go around the exact words a person says.", "hard"),
]


def gen_grammar_direct(rng):
    out = []
    for qtext, correct, distractors, explanation, difficulty in GRAMMAR_DIRECT:
        out.append(make_question(SUBJECT, GRAMMAR, qtext, correct, distractors, explanation, difficulty, rng))
    return out


# =============================================================== Literary Elements

FIGURATIVE_LANGUAGE = {
    "a simile (a comparison using 'like' or 'as')": [
        "Her smile was as bright as the sun.", "He ran like the wind.", "The ice was as cold as steel.",
        "The classroom was as quiet as a library.", "She is as brave as a lion.",
    ],
    "a metaphor (a comparison NOT using 'like' or 'as')": [
        "The classroom was a zoo during the fire drill.", "Time is money.", "His room is a disaster area.",
        "The stars were diamonds scattered across the sky.", "Her voice is music to my ears.",
    ],
    "personification (giving human qualities to something non-human)": [
        "The wind whispered through the trees.", "The old car groaned as it started.",
        "The flowers danced in the breeze.", "The sun smiled down on the town.", "The thunder growled overhead.",
    ],
    "hyperbole (an obvious exaggeration for effect)": [
        "I've told you a million times to clean your room.", "This backpack weighs a ton.",
        "I'm so hungry I could eat a horse.", "Her feet were killing her after the race.", "He ran faster than the speed of light.",
    ],
    "onomatopoeia (a word that imitates a sound)": [
        "The bees buzzed around the flowers.", "The balloon popped loudly.", "The bacon sizzled in the pan.",
        "The dog's tags jingled as it ran.", "Thunder crashed outside the window.",
    ],
    "alliteration (repeating the same beginning sound in nearby words)": [
        "Sally sells seashells by the seashore.", "Peter Piper picked a peck of pickled peppers.",
        "The slippery snake slid silently.", "Big brown bears bounced by.",
    ],
    "an idiom (a phrase that doesn't mean exactly what the words say)": [
        "It's raining cats and dogs outside.", "That test was a piece of cake.",
        "Let's just break the ice at the party.", "He's feeling under the weather today.",
    ],
}


def gen_figurative_language(rng, target):
    out = []
    seen = set()
    device_names = list(FIGURATIVE_LANGUAGE.keys())
    for device, sentences in FIGURATIVE_LANGUAGE.items():
        other_sentences = [s for d in device_names if d != device for s in FIGURATIVE_LANGUAGE[d]]
        for sentence in sentences:
            key = (device, sentence)
            if key in seen:
                continue
            seen.add(key)
            distractors = rng.sample(other_sentences, 3)
            device_label = device.split(" (")[0]
            qtext = f"Which sentence uses {device_label}?"
            explanation = f"'{sentence}' is an example of {device}."
            difficulty = "medium" if device_label in ("a simile", "onomatopoeia") else "hard"
            out.append(make_question(SUBJECT, LITERARY, qtext, sentence, distractors, explanation, difficulty, rng))
    rng.shuffle(out)
    return out[:target] if target else out


LITERARY_TERMS = {
    "Plot": "the sequence of events that happen in a story",
    "Theme": "the underlying lesson or message of a story",
    "Setting": "the time and place where a story happens",
    "Character": "a person or animal that takes part in the action of a story",
    "Conflict": "the main problem or struggle a character faces in a story",
    "Resolution": "the part of a story where the main problem is solved",
    "Protagonist": "the main character a story usually follows",
    "Antagonist": "a character or force that opposes the main character",
    "Point of view": "the perspective from which a story is told",
    "Narrator": "the person or voice that tells the story",
}
GENRE_TERMS = {
    "Fiction": "a story that comes from the author's imagination, not real events",
    "Nonfiction": "writing based on facts and real events",
    "Fantasy": "fiction that includes magical or impossible elements",
    "Mystery": "a story that centers on solving a puzzling crime or unexplained event",
    "Biography": "the true story of a real person's life, written by someone else",
    "Autobiography": "the true story of a person's life, written by that person",
    "Poetry": "writing arranged in lines and often using rhythm, rhyme, or vivid imagery",
    "Fable": "a short story, often with animal characters, that teaches a moral lesson",
    "Myth": "a traditional story, often explaining natural events, involving gods or heroes",
}


def gen_term_definitions(rng, term_dict, topic, difficulty):
    out = []
    names = list(term_dict.keys())
    for term, definition in term_dict.items():
        others = [t for t in names if t != term]
        if len(others) < 3:
            continue
        distractors = rng.sample(others, 3)
        qtext = f"What is the term for {definition}?"
        explanation = f"{term} is {definition}."
        out.append(make_question(SUBJECT, topic, qtext, term, distractors, explanation, difficulty, rng))

        def_distractors = [term_dict[d] for d in distractors]
        qtext2 = f"What does the term '{term}' mean in a story?" if topic == LITERARY else f"What does the term '{term}' mean?"
        out.append(make_question(SUBJECT, topic, qtext2, definition.capitalize(), [d.capitalize() for d in def_distractors],
                                  f"'{term}' means {definition}.", difficulty, rng))
    return out


# =============================================================== Writing & Composition

WRITING_TERMS = {
    "Topic sentence": "the sentence that states the main idea of a paragraph",
    "Supporting detail": "a fact or example that backs up the main idea of a paragraph",
    "Draft": "an early, unfinished version of a piece of writing",
    "Revise": "to improve a piece of writing's ideas, organization, and word choice",
    "Edit": "to fix a piece of writing's spelling, grammar, and punctuation",
    "Publish": "to share a finished piece of writing with an audience",
    "Transition word": "a word or phrase that connects ideas between sentences, like 'however' or 'next'",
    "Conclusion": "the closing part of a piece of writing that wraps up the main ideas",
    "Thesis": "a sentence that states the main point or argument of a piece of writing",
    "Introduction": "the opening part of a piece of writing that hooks the reader and states the topic",
}

WRITING_DIRECT = [
    ("Which is the best topic sentence for a paragraph about recycling?",
     "\"Recycling helps protect our planet in many ways.\"",
     ["\"I like pizza.\"", "\"Yesterday was sunny.\"", "\"My dog is brown.\""],
     "A topic sentence should introduce the paragraph's main idea — here, that's recycling and the planet.", "easy"),
    ("Which sentence would best be used as a transition between two paragraphs?",
     "\"In addition to saving water, recycling also saves energy.\"",
     ["\"Recycling is good.\"", "\"My favorite color is blue.\"", "\"The bin is green.\""],
     "'In addition to' connects the new idea (saving energy) to the previous paragraph's idea (saving water).", "hard"),
    ("What should a writer focus on during the revising stage?",
     "Improving ideas, organization, and word choice",
     ["Publishing the final copy", "Checking spelling only", "Choosing a topic"],
     "Revising means strengthening ideas, structure, and wording before final edits.", "hard"),
    ("What should a writer focus on during the editing stage?",
     "Fixing spelling, grammar, and punctuation mistakes",
     ["Coming up with a brand new topic", "Rewriting the whole piece from scratch", "Choosing a title only"],
     "Editing is the proofreading stage, focused on correctness rather than big idea changes.", "medium"),
    ("Which sentence gives the most specific, descriptive detail?",
     "\"The bright orange kite soared high above the sandy beach.\"",
     ["\"The kite went up.\"", "\"There was a kite.\"", "\"A kite flew.\""],
     "Specific details like color ('bright orange'), location ('sandy beach'), and precise verbs ('soared') make writing more vivid.", "medium"),
    ("Which is a strong concluding sentence for a paragraph about a class trip to the zoo?",
     "\"Our trip to the zoo was an unforgettable day full of amazing animals.\"",
     ["\"The zoo has animals.\"", "\"I woke up early that day.\"", "\"Buses are yellow.\""],
     "A strong conclusion wraps up the paragraph's main idea and feeling.", "medium"),
    ("What is the purpose of an introduction in a piece of writing?",
     "To hook the reader's interest and introduce the topic",
     ["To fix grammar mistakes", "To list every supporting detail in order", "To end the piece with a summary"],
     "An introduction grabs the reader's attention and previews what the writing is about.", "medium"),
    ("Which of these is an opinion, not a fact?",
     "\"Chocolate ice cream is the best flavor.\"",
     ["\"Ice cream is a frozen dessert.\"", "\"Ice cream is often made with milk and sugar.\"", "\"Ice cream must be kept cold.\""],
     "'Best flavor' is a personal judgment, not something that can be proven true or false — that makes it an opinion.", "medium"),
    ("Which sentence is written in a formal tone appropriate for a school report?",
     "\"The rainforest contains millions of unique species of plants and animals.\"",
     ["\"Rainforests are, like, super packed with animals and stuff.\"", "\"OMG the rainforest has SO many animals!\"", "\"Rainforests got tons of critters, ya know?\""],
     "Formal writing avoids slang and casual expressions, using clear, precise language instead.", "hard"),
]


def gen_writing_direct(rng):
    out = []
    for qtext, correct, distractors, explanation, difficulty in WRITING_DIRECT:
        out.append(make_question(SUBJECT, WRITING, qtext, correct, distractors, explanation, difficulty, rng))
    return out


# =============================================================== Reading Comprehension

READING_SKILL_TERMS = {
    "Main idea": "the most important point a passage is mostly about",
    "Inference": "a conclusion a reader makes using text clues and their own knowledge, even though it isn't stated directly",
    "Context clues": "hints in the surrounding words and sentences that help explain an unfamiliar word",
    "Cause and effect": "a text structure that shows why something happened (cause) and what happened as a result (effect)",
    "Compare and contrast": "a text structure that shows how two or more things are alike and different",
    "Summarize": "to briefly retell the most important parts of a text in your own words",
    "Author's purpose": "the reason an author wrote a text — to inform, persuade, or entertain",
    "Fact": "a statement that can be proven true",
    "Opinion": "a statement of someone's personal belief or feeling that cannot be proven true or false",
}


def gen_reading_skill_terms(rng):
    return gen_term_definitions(rng, READING_SKILL_TERMS, READING, "medium")


# --- Passages: each is (title, text, [ (question, correct, distractors, explanation, difficulty), ... ])
PASSAGES = [
    (
        "The New Kid",
        "Maria's hands were sweaty as she walked into her new classroom. She didn't know a single "
        "person, and everyone else seemed to already have their friends. She sat down at an empty desk "
        "near the window and stared at her notebook, hoping no one would notice how nervous she felt. "
        "Then a boy named Devon leaned over and whispered, 'I like your backpack. Did you just move here?' "
        "Maria's shoulders relaxed a little, and for the first time that morning, she smiled.",
        [
            ("How does Maria most likely feel at the start of the passage?", "Nervous", ["Excited", "Bored", "Angry"],
             "Her 'sweaty hands' and hoping no one would notice her feelings show she is nervous.", "easy"),
            ("What can you infer caused Maria to relax and smile?", "Devon being friendly to her",
             ["The teacher starting class", "Finding her notebook", "The bell ringing"],
             "Right after Devon spoke kindly to her, her shoulders relaxed and she smiled — the text implies his kindness caused the change.", "medium"),
            ("What is the main idea of this passage?", "A nervous new student starts to feel better after a classmate is kind to her",
             ["A boy loses his backpack at school", "A teacher assigns a seating chart", "A girl learns to read a map"],
             "The passage centers on Maria's nervousness as a new student and how Devon's kindness helps her feel more comfortable.", "medium"),
            ("What does the word 'relaxed' suggest about how Maria's body had been before?", "Tense or stiff from nervousness",
             ["Sleepy and tired", "Sick with a cold", "Cold from the weather"],
             "If her shoulders 'relaxed,' they must have been tense beforehand — a sign of nervousness.", "hard"),
        ],
    ),
    (
        "Saving the Coral Reefs",
        "Coral reefs are sometimes called the 'rainforests of the sea' because they are home to thousands "
        "of different ocean species. But many reefs around the world are dying. Warmer ocean water can "
        "cause corals to lose their bright colors in a process called bleaching. Once bleached, coral is "
        "much more likely to die. Scientists are working to protect reefs by growing new coral in labs and "
        "replanting it in the ocean. Everyday people can help too, by using less plastic and being careful "
        "about chemicals that wash into rivers and oceans.",
        [
            ("Why are coral reefs called the 'rainforests of the sea'?", "Because they are home to thousands of species",
             ["Because they grow very tall", "Because they only exist near rainforests", "Because they produce oxygen for the ocean"],
             "The passage directly states reefs are called this because so many species live there.", "easy"),
            ("What is the main cause of coral bleaching described in the passage?", "Warmer ocean water",
             ["Too much sunlight", "Too many fish", "Cold ocean currents"],
             "The passage states that warmer ocean water causes corals to lose their color, or bleach.", "medium"),
            ("What is the author's purpose in writing this passage?", "To inform readers about coral reefs and how to help protect them",
             ["To entertain readers with a made-up ocean story", "To persuade readers to become scientists", "To describe a vacation to a coral reef"],
             "The passage explains facts about reefs and offers real ways to help, which is meant to inform.", "medium"),
            ("Based on the passage, what can you infer about bleached coral?", "It is in danger and more likely to die than healthy coral",
             ["It is actually healthier than colorful coral", "It will always turn back to its normal color quickly", "It only happens in freshwater rivers"],
             "The passage says bleached coral 'is much more likely to die,' implying it is in a dangerous state.", "hard"),
        ],
    ),
    (
        "The Lemonade Stand",
        "Jayden wanted to buy a new video game, but he didn't have enough money saved up. His older sister "
        "suggested he start a lemonade stand. On the first day, Jayden only sold three cups because his sign "
        "was hard to read from the street. He made a bigger, brighter sign the next day, and sales tripled. "
        "By the end of the week, Jayden had earned enough money for the game — and he decided to save the "
        "extra money he made instead of spending all of it.",
        [
            ("Why did Jayden sell only three cups of lemonade on the first day?", "His sign was hard to read from the street",
             ["He ran out of lemons", "It was raining that day", "Nobody likes lemonade"],
             "The passage directly states his sign was hard to read from the street.", "easy"),
            ("What lesson does this passage most likely teach?", "Making improvements can lead to better results",
             ["Selling lemonade is always easy", "Video games are a waste of money", "Signs are not important for a business"],
             "Jayden improved his sign and his sales tripled, showing that making changes can improve results.", "medium"),
            ("What financial choice did Jayden make at the end of the passage?", "He decided to save some of his extra earnings",
             ["He spent all his money on lemons", "He gave his money away", "He borrowed money from his sister"],
             "The passage states he 'decided to save the extra money he made instead of spending all of it.'", "medium"),
        ],
    ),
    (
        "How Bees Make Honey",
        "Honeybees visit flowers to collect a sweet liquid called nectar. Back at the hive, the bees pass "
        "the nectar from bee to bee, and special enzymes in their bodies begin changing it. The bees then "
        "store the nectar in honeycomb cells and fan it with their wings to remove extra water. Once the "
        "liquid has thickened, it becomes honey, and the bees seal the cell with wax to keep it fresh. A "
        "single bee might visit hundreds of flowers in one trip to gather enough nectar.",
        [
            ("What do bees collect from flowers to eventually make honey?", "Nectar", ["Pollen only", "Water", "Wax"],
             "The passage states bees collect 'a sweet liquid called nectar.'", "easy"),
            ("Why do bees fan the nectar with their wings?", "To remove extra water so it thickens into honey",
             ["To cool down the hive", "To attract more bees", "To clean the honeycomb"],
             "The passage explains fanning removes extra water, thickening the liquid into honey.", "medium"),
            ("What is this passage mostly about?", "The steps bees take to turn nectar into honey",
             ["The dangers bees face in nature", "Different types of flowers bees like", "How to build a beehive"],
             "The whole passage describes the process, step by step, of how bees make honey from nectar.", "medium"),
            ("What text structure does this passage mainly use?", "Sequence (steps in order)",
             ["Compare and contrast", "Cause and effect only", "Problem and solution"],
             "The passage walks through the honey-making process in a step-by-step order, which is a sequence structure.", "hard"),
        ],
    ),
    (
        "A Surprise Storm",
        "The sky had been clear all morning, so Priya and her dad decided to hike to the top of the ridge. "
        "Halfway up the trail, dark clouds rolled in seemingly out of nowhere, and thunder rumbled in the "
        "distance. Priya's dad checked his weather app and frowned. 'We need to turn back now,' he said. They "
        "hurried down the trail just as the first raindrops began to fall, reaching their car right before "
        "the storm broke fully.",
        [
            ("What is the main problem in this passage?", "A storm suddenly appears while Priya and her dad are hiking",
             ["Priya gets lost on the trail", "Priya's dad forgets the car keys", "The trail is too steep to climb"],
             "The central conflict is the unexpected storm interrupting their hike.", "easy"),
            ("How does Priya's dad respond to the changing weather?", "He decides they should turn back immediately",
             ["He ignores the clouds and keeps hiking", "He calls for help", "He sets up a tent to wait it out"],
             "The passage says he frowned and said, 'We need to turn back now.'", "medium"),
            ("What can you infer about how Priya's dad felt when he checked the weather app?", "Concerned or worried",
             ["Excited and happy", "Bored", "Confused about how to use the app"],
             "His frown when checking the app suggests concern about the coming storm.", "hard"),
        ],
    ),
    (
        "The Class Garden",
        "Ms. Alvarez's class decided to plant a vegetable garden behind the school. Each student was "
        "responsible for watering the plants twice a week and pulling any weeds they saw. At first, the "
        "tomato plants grew slowly, but after a few weeks of steady care, they became tall and full of "
        "fruit. By the end of the school year, the class had grown enough tomatoes, peppers, and lettuce "
        "to share a salad with the whole school.",
        [
            ("What were students responsible for doing in the garden?", "Watering the plants and pulling weeds",
             ["Painting the garden fence", "Building a greenhouse", "Selling the vegetables"],
             "The passage states each student watered plants twice a week and pulled weeds.", "easy"),
            ("What happened to the tomato plants over time?", "They grew slowly at first, then became tall and full of fruit",
             ["They died within a week", "They grew instantly overnight", "They never produced any tomatoes"],
             "The passage describes slow early growth followed by the plants becoming tall and full of fruit.", "medium"),
            ("What is the main idea of this passage?", "A class garden succeeds through the students' consistent care",
             ["Tomatoes are hard to grow anywhere", "Ms. Alvarez does all the gardening herself", "The school has no outdoor space"],
             "The passage focuses on how the students' steady care led to a successful garden.", "medium"),
        ],
    ),
    (
        "The Talent Show",
        "Ben had practiced his magic tricks for weeks before the school talent show, but backstage, his "
        "hands began to shake. He peeked through the curtain and saw the packed auditorium. His best friend, "
        "Owen, noticed and gave him a thumbs up. 'You've got this,' Owen whispered. When Ben's name was "
        "called, he took a deep breath, walked onstage, and performed his best trick yet — the audience "
        "erupted into applause.",
        [
            ("How does Ben feel backstage before his performance?", "Nervous", ["Confident", "Angry", "Sleepy"],
             "His shaking hands show that he is nervous before performing.", "easy"),
            ("What effect does Owen's encouragement have on Ben?", "It helps calm and encourage him before he performs",
             ["It makes Ben more nervous", "It causes Ben to leave the show", "It has no effect on Ben"],
             "Right after Owen's encouragement, Ben takes a deep breath and performs his best trick, suggesting the encouragement helped.", "medium"),
            ("What can you infer from the audience's reaction at the end?", "Ben's performance was a success",
             ["The audience did not enjoy the trick", "Ben forgot his trick", "The show was cancelled"],
             "The audience erupting into applause implies the trick went very well.", "medium"),
        ],
    ),
    (
        "Migration of Monarch Butterflies",
        "Every fall, millions of monarch butterflies travel from the United States and Canada all the way "
        "to central Mexico, a journey of up to 3,000 miles. No single butterfly makes the whole round trip; "
        "instead, it takes several generations to complete the full migration cycle. Scientists still aren't "
        "completely sure how monarchs find their way, but they believe the butterflies use the position of "
        "the sun and Earth's magnetic field to help navigate.",
        [
            ("About how far do monarch butterflies travel during migration?", "Up to 3,000 miles",
             ["About 300 miles", "About 30 miles", "About 30,000 miles"],
             "The passage states the journey is 'up to 3,000 miles.'", "easy"),
            ("What is surprising about which butterflies complete the migration, according to the passage?", "No single butterfly makes the whole round trip; it takes several generations",
             ["Only baby butterflies migrate", "Butterflies migrate in the spring, not fall", "Only male butterflies migrate"],
             "The passage specifically notes it takes several generations, not one butterfly, to complete the cycle.", "hard"),
            ("What do scientists believe helps monarchs navigate during migration?", "The position of the sun and Earth's magnetic field",
             ["Following other bird species", "Using landmarks like mountains only", "GPS trackers"],
             "The passage states scientists believe monarchs use the sun's position and Earth's magnetic field.", "medium"),
        ],
    ),
    (
        "The Library Card",
        "For his tenth birthday, Sam asked his parents for something unusual: his very own library card. At "
        "first his little brother laughed, saying a library card wasn't a real present. But every Saturday "
        "after that, Sam happily walked to the library and came home with a stack of new books. By the end "
        "of the summer, his little brother had asked for a library card of his own.",
        [
            ("What was unusual about Sam's birthday request?", "He asked for a library card instead of a typical toy or gift",
             ["He asked for a puppy", "He asked for money", "He asked for a new bike"],
             "The passage frames the library card as an 'unusual' request compared to typical gifts.", "easy"),
            ("How does the little brother's attitude change over the passage?", "He goes from mocking the gift to wanting a library card himself",
             ["He stays annoyed with Sam the whole time", "He never changes his mind", "He decides he hates reading"],
             "He starts by laughing at the gift, but by the end he asks for one too, showing his attitude changed.", "medium"),
            ("What is the main idea of this passage?", "An unusual gift ends up inspiring someone else to enjoy reading too",
             ["Birthdays are not important", "Libraries are closed on Saturdays", "Sam does not like to read"],
             "The passage centers on how Sam's love of his library card eventually influences his brother.", "medium"),
        ],
    ),
    (
        "Building an Igloo",
        "In some Arctic regions, the Inuit people have traditionally built igloos, or snow houses, as "
        "temporary winter shelters. Builders cut blocks of hard-packed snow and stack them in a spiral shape "
        "that curves inward, forming a dome. Surprisingly, the trapped air inside packed snow acts as an "
        "insulator, and body heat from the people inside can keep an igloo noticeably warmer than the freezing "
        "air outside.",
        [
            ("What material is used to build an igloo?", "Blocks of hard-packed snow", ["Bricks", "Wooden planks", "Ice cubes from a freezer"],
             "The passage states builders 'cut blocks of hard-packed snow.'", "easy"),
            ("Why might it seem surprising that an igloo can be warm inside?", "Because it's made entirely of snow, which people usually think of as cold",
             ["Because igloos have heaters built in", "Because igloos are built in summer", "Because igloos are made of wood"],
             "The passage calls it 'surprising' because trapped air in snow insulates, despite snow seeming like an odd material for warmth.", "hard"),
            ("What shape do builders arrange the snow blocks into?", "A spiral that curves inward into a dome",
             ["A square box", "A flat circle", "A tall tower"],
             "The passage describes blocks stacked 'in a spiral shape that curves inward, forming a dome.'", "medium"),
        ],
    ),
    (
        "The Science Fair Project",
        "Aaliyah wanted her science fair project to test whether plants grow better with tap water or "
        "rainwater. She planted two identical bean seeds in identical pots with the same soil and sunlight, "
        "watering one with tap water and one with rainwater every day. After two weeks, the plant watered "
        "with rainwater was two inches taller. Aaliyah concluded that, at least for her plants, rainwater "
        "helped them grow faster than tap water did.",
        [
            ("What was the independent variable in Aaliyah's experiment (the thing she changed)?", "The type of water used (tap vs. rainwater)",
             ["The type of soil", "The amount of sunlight", "The type of seed"],
             "Everything else was kept the same except which water was used, making that the independent variable.", "hard"),
            ("What did Aaliyah keep the same between her two plants?", "The pots, soil, and sunlight",
             ["The amount of water", "The type of water", "The type of seed and the water"],
             "The passage states the pots, soil, and sunlight were identical — only the water type differed.", "medium"),
            ("What conclusion did Aaliyah draw from her experiment?", "Rainwater helped her plants grow faster than tap water",
             ["Tap water is unsafe to drink", "Sunlight doesn't affect plant growth", "Both waters worked exactly the same"],
             "The passage states her conclusion directly: rainwater helped the plants grow faster.", "medium"),
        ],
    ),
    (
        "A Trip to Grandma's Farm",
        "Every summer, Noah stayed at his grandmother's farm for two weeks. He used to think farm chores "
        "sounded boring, but collecting eggs from the hens and feeding the goats quickly became his favorite "
        "part of the day. This year, his grandmother let him help plant a new row of sunflowers. Watching the "
        "tiny seeds he planted grow into towering flowers by August made Noah feel proud in a way video games "
        "never had.",
        [
            ("How did Noah's feelings about farm chores change over time?", "He used to think they sounded boring but grew to enjoy them",
             ["He always loved farm chores", "He never learned to enjoy them", "He refused to do any chores"],
             "The passage says he 'used to think farm chores sounded boring,' but they 'quickly became his favorite part.'", "medium"),
            ("What new activity did Noah get to do this year at the farm?", "Help plant a row of sunflowers",
             ["Milk a cow for the first time", "Drive a tractor", "Build a chicken coop"],
             "The passage states his grandmother let him help plant sunflowers this year.", "easy"),
            ("What can you infer about how Noah feels about video games by the end of the passage?", "He finds this real accomplishment more rewarding than video games",
             ["He thinks video games are more exciting than farming", "He wants to buy a new video game", "He no longer enjoys any games at all"],
             "The comparison 'in a way video games never had' implies this feeling of pride outweighs what video games give him — but doesn't mean he dislikes games entirely.", "hard"),
        ],
    ),
]


def gen_passage_questions(rng):
    out = []
    for title, text, questions in PASSAGES:
        for qtext, correct, distractors, explanation, difficulty in questions:
            full_qtext = f'Read the passage "{title}," then answer the question.\n\n{text}\n\n{qtext}'
            out.append(make_question(SUBJECT, READING, full_qtext, correct, distractors, explanation, difficulty, rng))
    return out


def generate_english_questions(total=300, easy_ratio=0.2, medium_ratio=0.5, hard_ratio=0.3):
    rng = random.Random(SEED)
    pool = []
    pool += gen_vocab_questions(rng)
    pool += gen_affix_questions(rng)
    pool += gen_subject_verb_agreement(rng, 60)
    pool += gen_contraction_questions(rng, 40)
    pool += gen_grammar_direct(rng)
    pool += gen_figurative_language(rng, None)
    pool += gen_term_definitions(rng, LITERARY_TERMS, LITERARY, "medium")
    pool += gen_term_definitions(rng, GENRE_TERMS, LITERARY, "medium")
    pool += gen_writing_direct(rng)
    pool += gen_term_definitions(rng, WRITING_TERMS, WRITING, "medium")
    pool += gen_reading_skill_terms(rng)
    pool += gen_passage_questions(rng)

    easy_n = round(total * easy_ratio)
    medium_n = round(total * medium_ratio)
    hard_n = total - easy_n - medium_n
    return select_balanced(pool, easy_n, medium_n, hard_n, rng)


if __name__ == "__main__":
    from collections import Counter
    qs = generate_english_questions()
    print("total:", len(qs))
    print("by difficulty:", Counter(q["difficulty"] for q in qs))
    print("by topic:", Counter(q["topic"] for q in qs))
    for q in qs[:6]:
        print("-", q["question_text"][:100].replace("\n", " "), "=>", q["correct_choice"])
