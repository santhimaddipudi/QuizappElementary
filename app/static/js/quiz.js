(function () {
  const wrap = document.querySelector(".quiz-wrap");
  if (!wrap) return;

  const subjectSlug = wrap.dataset.subjectSlug;

  const introPanel = document.getElementById("quiz-intro");
  const questionPanel = document.getElementById("quiz-question");
  const resultsPanel = document.getElementById("quiz-results");

  const startBtn = document.getElementById("start-btn");
  const nextBtn = document.getElementById("next-btn");
  const retryBtn = document.getElementById("retry-btn");
  const studentNameInput = document.getElementById("student-name");
  const quizLengthSelect = document.getElementById("quiz-length");

  const progressFill = document.getElementById("progress-fill");
  const questionMeta = document.getElementById("question-meta");
  const questionText = document.getElementById("question-text");
  const questionImageWrap = document.getElementById("question-image-wrap");
  const questionImage = document.getElementById("question-image");
  const choicesEl = document.getElementById("choices");
  const feedbackEl = document.getElementById("feedback");

  const scoreSummary = document.getElementById("score-summary");
  const resultsList = document.getElementById("results-list");

  let questions = [];
  let currentIndex = 0;
  let answers = [];
  let cycleReset = false;
  let selectedChoice = null;

  const seenKey = `quizSeen:${subjectSlug}`;

  function loadSeenIds() {
    try {
      const raw = localStorage.getItem(seenKey);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function saveSeenIds(ids) {
    try {
      localStorage.setItem(seenKey, JSON.stringify(ids));
    } catch (e) {
      // localStorage unavailable (e.g. private browsing) — no-repeat tracking just won't persist.
    }
  }

  function showPanel(panel) {
    [introPanel, questionPanel, resultsPanel].forEach((p) => (p.hidden = p !== panel));
  }

  async function startQuiz() {
    startBtn.disabled = true;
    startBtn.textContent = "Loading...";
    try {
      const count = quizLengthSelect ? quizLengthSelect.value : 10;
      const seen = loadSeenIds();
      const url = `/api/quiz/${subjectSlug}?count=${count}` + (seen.length ? `&exclude=${seen.join(",")}` : "");
      const res = await fetch(url);
      const data = await res.json();
      questions = data.questions;
      cycleReset = !!data.cycle_reset;
      currentIndex = 0;
      answers = [];
      showPanel(questionPanel);
      renderQuestion();
    } finally {
      startBtn.disabled = false;
      startBtn.textContent = "Start Quiz";
    }
  }

  function renderQuestion() {
    const q = questions[currentIndex];
    progressFill.style.width = `${(currentIndex / questions.length) * 100}%`;
    questionMeta.textContent = `Question ${currentIndex + 1} of ${questions.length}${q.topic ? " · " + q.topic : ""}`;
    questionText.textContent = q.question_text;

    if (q.image_path) {
      questionImage.src = `/static/${q.image_path}`;
      questionImage.alt = "Diagram for this question";
      questionImageWrap.hidden = false;
    } else {
      questionImageWrap.hidden = true;
      questionImage.removeAttribute("src");
    }

    selectedChoice = null;
    feedbackEl.hidden = true;
    feedbackEl.className = "feedback";

    choicesEl.innerHTML = "";
    const letters = ["A", "B", "C", "D"];
    const labels = [q.choice_a, q.choice_b, q.choice_c, q.choice_d];

    letters.forEach((letter, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "choice-btn";
      btn.textContent = `${letter}. ${labels[i]}`;
      btn.addEventListener("click", () => selectChoice(letter, btn));
      choicesEl.appendChild(btn);
    });
  }

  function selectChoice(letter, btn) {
    const q = questions[currentIndex];
    Array.from(choicesEl.children).forEach((b) => (b.disabled = true));

    selectedChoice = letter;
    answers.push({ question_id: q.id, choice: letter, image_path: q.image_path || null });

    // Optimistic client-side feedback; the server re-checks on submit.
    btn.classList.add("chosen");

    feedbackEl.hidden = false;
    feedbackEl.textContent = "Answer recorded! Click Next to continue.";
    feedbackEl.className = "feedback correct";
  }

  function handleNextClick() {
    if (!selectedChoice) {
      feedbackEl.hidden = false;
      feedbackEl.textContent = "Please select an option before continuing.";
      feedbackEl.className = "feedback warning";
      return;
    }
    nextQuestion();
  }

  function nextQuestion() {
    currentIndex += 1;
    if (currentIndex >= questions.length) {
      submitQuiz();
    } else {
      renderQuestion();
    }
  }

  async function submitQuiz() {
    progressFill.style.width = "100%";
    const res = await fetch("/api/quiz/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: subjectSlug,
        student_name: studentNameInput.value,
        answers,
      }),
    });
    const data = await res.json();
    showResults(data);
  }

  function updateSeenIds() {
    const thisQuizIds = questions.map((q) => q.id);
    if (cycleReset) {
      // The pool ran low on never-seen questions and was topped up from older
      // ones, so treat this quiz as the start of a brand new no-repeat cycle.
      saveSeenIds(thisQuizIds);
    } else {
      const merged = new Set([...loadSeenIds(), ...thisQuizIds]);
      saveSeenIds([...merged]);
    }
  }

  function showResults(data) {
    updateSeenIds();
    showPanel(resultsPanel);
    const pct = Math.round((data.score / data.total) * 100);
    scoreSummary.textContent = `You scored ${data.score} out of ${data.total} (${pct}%)`;
    if (cycleReset) {
      scoreSummary.textContent += " — you've now seen every question in this subject, so a new round just started!";
    }

    resultsList.innerHTML = "";
    data.results.forEach((r, i) => {
      const item = document.createElement("div");
      item.className = `result-item ${r.is_correct ? "correct" : "incorrect"}`;
      const imagePath = answers[i] && answers[i].image_path;
      item.innerHTML = `
        <p><strong>Q${i + 1}:</strong> ${r.question_text}</p>
        ${imagePath ? `<img class="result-image" src="/static/${imagePath}" alt="Diagram for this question">` : ""}
        <p>${r.is_correct ? "✅ Correct" : `❌ You chose ${r.chosen}, correct answer was ${r.correct_choice}`}</p>
        ${r.explanation ? `<p class="explanation">${r.explanation}</p>` : ""}
      `;
      resultsList.appendChild(item);
    });
  }

  startBtn.addEventListener("click", startQuiz);
  nextBtn.addEventListener("click", handleNextClick);
  retryBtn.addEventListener("click", () => {
    showPanel(introPanel);
  });
})();
