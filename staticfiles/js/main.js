function startTimer(durationInSeconds, timerKey) {
    const timerElement = document.getElementById('timer');
    const alarmSound = new Audio("/static/audio/ringing.mp3");
    const savedTime = localStorage.getItem(timerKey);
    let timeLeft = savedTime !== null ? parseInt(savedTime) : durationInSeconds;
    const lastDate = localStorage.getItem('timerDate');
    const currentDate = new Date().toDateString();
    if (lastDate !== currentDate) {
        timeLeft = durationInSeconds;
        localStorage.setItem('timerDate', currentDate);
    }
    let timerInterval;
    function updateTimer() {
        localStorage.setItem(timerKey, timeLeft);
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        const percentage = timeLeft / durationInSeconds;
        if (percentage > 0.75) {
            timerElement.style.color = 'green';
        } else if (percentage > 0.5) {
            timerElement.style.color = 'yellow';
        } else if (percentage > 0.25) {
            timerElement.style.color = 'orange';
        } else {
            timerElement.style.color = 'red';
        }
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            if (alarmSound) {
                alarmSound.play();
            }
        }
        timeLeft--;
    }
    function handleVisibilityChange() {
        if (document.visibilityState === 'visible') {
            timerInterval = setInterval(updateTimer, 1000);
        } else {
            clearInterval(timerInterval);
        }
    }
    document.addEventListener('visibilitychange', handleVisibilityChange);
    if (document.visibilityState === 'visible') {
        timerInterval = setInterval(updateTimer, 1000);
    }
}
startTimer(3600, 'homePageTimer');

const quotes = [
    "\"Great Minds Often take the road less traveled\"",
    "\"The journey of a 1,000 mi. begins with a single step\"",
    "\"Success is not final, failure is not fatal\"",
    "\"Believe you can and you're halfway there\"",
    "\"There's no shortcut to a place worth going\"",
];

let currentIndex = 0;
const quoteText = document.getElementById("quote-text");
const pokeLeft = document.getElementById("poke-left");
const pokeRight = document.getElementById("poke-right");

function updateQuote(index) {
    quoteText.style.opacity = 0;
    quoteText.style.transform = "translateY(20px)";
    setTimeout(() => {
        quoteText.textContent = quotes[index];
        quoteText.style.opacity = 1;
        quoteText.style.transform = "translateY(0)";
    }, 500);
}

function startAutoLoop() {
    setInterval(() => {
        currentIndex = (currentIndex + 1) % quotes.length;
        updateQuote(currentIndex);
    }, 50000);
}

pokeLeft.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + quotes.length) % quotes.length;
    updateQuote(currentIndex);
});

pokeRight.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % quotes.length;
    updateQuote(currentIndex);
});

updateQuote(currentIndex);
startAutoLoop();

const modal = document.getElementById("postModal");
const trigger = document.querySelector(".post-form");
const closeButton = document.querySelector(".close-btn");
const cancelBtn = document.querySelector(".cancel-btn");

if (modal) {
    trigger.addEventListener("click", () => {
        modal.style.display = "flex";
        document.body.style.overflow = "hidden";
    });

    closeButton.addEventListener("click", () => {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    });

    if (cancelBtn) {
        cancelBtn.addEventListener("click", () => {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        });
    } else {
        console.warn("Cancel button not found in DOM!");
    }

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }
    });
} else {
    console.warn("Post modal not found in DOM!");
}
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menu = document.querySelector('.hamburger-menu');
    sidebar.classList.toggle('show');
    menu.classList.toggle('active');
}

document.getElementById('sharebtn').addEventListener('click', function() {
    const rawText = "https://infinitfolio.site/posts/{{ post.id }}";
    navigator.clipboard.writeText(rawText)
    .then(function() {
        alert('Text copied to clipboard!');
    })
    .catch(function(error) {
        console.error('Failed to copy text: ', error);
    });
});

function copy(text){
    navigator.clipboard.writeText(text)
    .then(function() {
        alert('Post copied to clipboard!');
    })
    .catch(function(error) {
        console.error('Failed to copy text: ', error);
    });
}

const toggleThemeBtn = document.getElementById('toggleTheme');
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    toggleThemeBtn.textContent = '☀️';
}
toggleThemeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    if (document.body.classList.contains('dark-mode')) {
        toggleThemeBtn.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    } else {
        toggleThemeBtn.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    }
});

var simplemde = new SimpleMDE({ 
    element: document.getElementById("postContent"), 
    spellChecker: true, 
});