let currentQuestionIndex = 0;
let selectedAnswers = [];
const questions = [
    {
        question: "What is 2 + 2?",
        options: ["3", "4", "5", "6"],
        answer: 1
    },
    {
        question: "What is the capital of France?",
        options: ["Berlin", "Madrid", "Paris", "Rome"],
        answer: 2
    }
];

function loadQuestion() {
    const questionElement = document.getElementById("question");
    const optionsElement = document.getElementById("options");
    questionElement.textContent = questions[currentQuestionIndex].question;
    optionsElement.innerHTML = "";
    
    questions[currentQuestionIndex].options.forEach((option, index) => {
        const button = document.createElement("button");
        button.textContent = option;
        button.classList.add("option");
        button.onclick = () => selectOption(index);
        if (selectedAnswers[currentQuestionIndex] === index) {
            button.style.backgroundColor = "#007bff";
            button.style.color = "white";
        }
        optionsElement.appendChild(button);
    });
}

function selectOption(selectedIndex) {
    selectedAnswers[currentQuestionIndex] = selectedIndex;
    loadQuestion();
}

function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion();
    }
}

function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        loadQuestion();
    }
}

function submitTest() {
    let score = 0;
    questions.forEach((question, index) => {
        if (selectedAnswers[index] === question.answer) {
            score++;
        }
    });
    alert(`Test submitted! Your score: ${score} / ${questions.length}`);
}

document.addEventListener("DOMContentLoaded", loadQuestion);