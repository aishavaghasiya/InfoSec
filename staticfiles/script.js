// Toggle mobile navigation menu
function toggleMenu() {
    document.querySelector('.nav-links').classList.toggle('active');
}

// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function() {
    const box = document.querySelector('.box');
    const toggleButton = document.getElementById('toggleButton');
    const typingText = document.getElementById("typing-text");

    // Ensure the box exists before applying animation
    if (box) {
        box.classList.add("show"); // Add 'show' class for animation
    }

    // Toggle background color when button is clicked
    if (toggleButton && box) {
        toggleButton.addEventListener('click', function() {
            const currentColor = window.getComputedStyle(box).backgroundColor;
            box.style.backgroundColor = currentColor === 'rgb(76, 175, 80)' ? '#2196F3' : '#4CAF50'; // Toggle between green and blue
        });
    }

    // Typing Effect for Heading
    if (typingText) {
        const text = "InfoSec – Defend, Protect, Secure";
        let index = 0;

        function typeEffect() {
            if (index < text.length) {
                typingText.innerHTML += text.charAt(index);
                index++;
                setTimeout(typeEffect, 100); // Adjust speed of typing
            }
        }

        typeEffect(); // Start typing effect
    }
});
