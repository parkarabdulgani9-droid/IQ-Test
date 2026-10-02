let questionBank = [];
let currentIdx = 0;
let score = 0;
let timeLeft = 20;
let timer;
let answered = false;

async function startGame() {
    try {
        const response = await fetch("/get_questions");
        if (!response.ok) {
            throw new Error("Unable to load questions.");
        }
        questionBank = await response.json();
        if(!Array.isArray(questionBank) || questionBank.length === 0){
            throw new Error("No questions available")   
        }

        document.getElementById("start-screen").classList.add("hidden");
        document.getElementById("result-screen").classList.add("hidden");
        document.getElementById("quiz-screen").classList.remove("hidden");

        currentIdx = 0;
        score = 0;

        loadQuestion();

    } catch(error) {
        console.error(error);
        alert("Unable to load the quiz. Please try again.");
    }
}

function loadQuestion() {
    if (currentIdx >= questionBank.length) {
        endLevel();
        return;
    }
    answered = false;
    const data = questionBank[currentIdx];
    document.getElementById("question-text").innerText = data.q;
    document.getElementById("question-counter").innerText = `Question ${currentIdx + 1}/${questionBank.length}`;
    const progress = (currentIdx / questionBank.length) * 100;
    document.getElementById("progress-fill").style.width = `${(currentIdx / questionBank.length) * 100}%`;
    const container = document.getElementById("options-container");

    container.innerHTML = "";

    data.a.forEach((option, index) => {
        const button = document.createElement("button");
        button.className = "option-btn";
        button.innerText = option;
        button.onclick = () => handleSelect(index, button);
        container.appendChild(button);
    });
    startTimer();
}

function startTimer() {
<<<<<<< HEAD
=======
    timeLeft = 20;
    document.getElementById('timer').innerText = `Time: ${timeLeft}s`;
>>>>>>> f5de1bf (My changes)
    clearInterval(timer);
    timeLeft = 15;
    document.getElementById("timer").innerText = `Time: ${timeLeft}s`;
    timer = setInterval(() => {
        timeLeft--;
        document.getElementById("timer").innerText = `Time: ${timeLeft}s`;
        if (timeLeft <= 0) {
            clearInterval(timer);
            handleSelect(-1);
        }
    }, 1000);
}

function handleSelect(index, selectedButton = null) {
    if (answered) {
        return;
    }
    answered = true;
    clearInterval(timer);
    const correctIndex = questionBank[currentIdx].correct;
    const buttons = document.querySelectorAll(".option-btn");
    buttons.forEach(button => {
        button.disabled = true;
    });

    if (index === -1) {
        currentIdx++;
        loadQuestion();
        return;
    }
    else if (index === correctIndex) {
        selectedButton.classList.add("correct");
        score += 10 + timeLeft;
    }
    else {
        selectedButton.classList.add("wrong");
        buttons[correctIndex].classList.add("correct");
    }
    setTimeout(() => {
        currentIdx++;
        loadQuestion();
    }, 1000);
}

async function endLevel() {

    clearInterval(timer);

    document.getElementById("quiz-screen").classList.add("hidden");
    document.getElementById("result-screen").classList.remove("hidden");
    document.getElementById("final-score").innerText = score;

    let message;
    if (score >= 200) {
        message = "Excellent logical thinking!";
    } else if (score >= 120) {
        message = "Solid analytical skills!";
    } else {
        message = "Keep training your brain!";
    }
    document.getElementById("feedback-text").innerText = message;

    try{
        const response = await fetch('/save_result',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                score: score
            })
        });
        const data = await response.json();
        if(!response.ok){
            console.log("Failed to save result", data);
        }
    } catch (error){
        console.error("Error saving result: ", error);
    }
}