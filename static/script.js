let questionBank = [];
let currentIdx = 0;
let score = 0;
let timeLeft = 15;
let timer;

// Fetch questions from Flask API
async function startGame() {
    const response = await fetch('/get_questions');
    questionBank = await response.json();
    
    document.getElementById('start-screen').classList.add('hidden');
    document.getElementById('result-screen').classList.add('hidden');
    document.getElementById('quiz-screen').classList.remove('hidden');
    currentIdx = 0;
    score = 0;
    loadQuestion();
}

function loadQuestion() {
    if (currentIdx >= questionBank.length) return endLevel();
    
    const data = questionBank[currentIdx];
    document.getElementById('question-text').innerText = data.q;
    document.getElementById('question-counter').innerText = `Question ${currentIdx + 1}/${questionBank.length}`;
    document.getElementById('progress-fill').style.width = `${((currentIdx) / questionBank.length) * 100}%`;
    
    const container = document.getElementById('options-container');
    container.innerHTML = '';
    
    data.a.forEach((opt, i) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.innerText = opt;
        btn.onclick = () => handleSelect(i, btn);
        container.appendChild(btn);
    });

    startTimer();
}

function startTimer() {
    timeLeft = 15;
    document.getElementById('timer').innerText = `Time: ${timeLeft}s`;
    clearInterval(timer);
    timer = setInterval(() => {
        timeLeft--;
        document.getElementById('timer').innerText = `Time: ${timeLeft}s`;
        if (timeLeft <= 0) handleSelect(-1);
    }, 1000);
}

function handleSelect(idx, btn) {
    clearInterval(timer);
    const correct = questionBank[currentIdx].correct;
    const buttons = document.querySelectorAll('.option-btn');
    
    buttons.forEach(b => b.disabled = true);

    if (idx === -1) {
        currentIdx++;
        loadQuestion();
        return;
    }

    if (idx === correct) {
        if (btn) btn.classList.add('correct');
        score += (10 + timeLeft);
    } else {
        if (btn) btn.classList.add('wrong');
        buttons[correct].classList.add('correct');
    }

    setTimeout(() => {
        currentIdx++;
        loadQuestion();
    }, 1200);
}

function endLevel() {
    document.getElementById('quiz-screen').classList.add('hidden');
    document.getElementById('result-screen').classList.remove('hidden');
    document.getElementById('final-score').innerText = score;
    
    let msg = score > 200 ? "Genius Level Logic!" : score > 120 ? "Solid Analytical Skills." : "Keep Training Your Brain.";
    document.getElementById('feedback-text').innerText = msg;
}