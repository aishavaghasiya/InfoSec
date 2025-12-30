// Toggle mobile navigation menu
function toggleMenu() {
    document.querySelector('.nav-links').classList.toggle('active');
}

// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function () {
    const box = document.querySelector('.box');
    const typingText = document.getElementById("typing-text");
    const socialIcons = document.getElementById("social-icons");
    const closeBtn = document.getElementById("closeBtn");
    const alertBox = document.getElementById("alertBox");
    const ipAddress = document.getElementById("ipAddress");
    const loading = document.getElementById("loading");
    const ipForm = document.getElementById("scanForm");
    const cards = document.querySelectorAll(".card");

    const contactForm = document.getElementById("contactForm");
    const successPopup = document.getElementById("successPopup");
    const successMessage = document.getElementById("successMessage");
    const popupOverlay = document.getElementById("popupOverlay");
    const serviceCards = document.querySelectorAll(".service-card");
    const image = document.querySelector(".about-image img");
    const image1 = document.querySelector(".mission-image img");
    const teamCards = document.querySelectorAll(".team-card");

    const passwordInput = document.getElementById("password");
    const strengthText = document.getElementById("strength-text");
    const progressBar = document.getElementById("progress-bar");

    const faqItems = document.querySelectorAll(".faq-item");


    faqItems.forEach((item) => {
        const question = item.querySelector(".faq-question");

        question.addEventListener("click", function () {
            // Toggle the active class for the clicked FAQ item
            item.classList.toggle("active");

            // Change the "+" to "-" when opened and vice versa
            const toggleIcon = item.querySelector(".faq-toggle");
            if (item.classList.contains("active")) {
                toggleIcon.textContent = "−"; // Minus sign when expanded
            } else {
                toggleIcon.textContent = "+"; // Plus sign when collapsed
            }
        });
    });

    // Ensure the box exists before applying animation
    if (box) {
        box.classList.remove("show");
        setTimeout(() => box.classList.add("show"), 100);
    }

    // Typing Effect for Heading
    if (typingText) {
        const text = "InfoSec – Defend, Protect, Secure !!";
        let index = 0;

        typingText.innerHTML = '<span id="text-content"></span><span class="cursor"></span>';
        const textContent = document.getElementById("text-content");
        const cursor = document.querySelector(".cursor");

        function typeEffect() {
            if (index < text.length) {
                textContent.innerHTML += text.charAt(index);
                index++;
                setTimeout(typeEffect, 100);
            }
        }

        typeEffect();
    }

    // Social Media Icons
    if (socialIcons) {
        const socialLinks = [
            { url: "https://github.com/Radhendelvadiya", iconClass: "fab fa-github" },
            { url: "https://www.facebook.com/radhen.patel.731/", iconClass: "fab fa-facebook" },
            { url: "https://www.linkedin.com/in/radhen-delvadiya-018886233/", iconClass: "fab fa-linkedin" },
            { url: "https://x.com/Radhen_103", iconClass: "fab fa-twitter" },
        ];

        socialLinks.forEach(link => {
            const a = document.createElement("a");
            a.href = link.url;
            a.target = "_blank";
            a.innerHTML = `<i class="${link.iconClass}"></i>`;
            socialIcons.appendChild(a);
        });
    }

    // Close Alert Box
    if (closeBtn && alertBox) {
        closeBtn.addEventListener("click", function () {
            alertBox.style.display = "none"; 
        });
    }

    // Show Loading Effect when scanning
    if (ipForm) {
        ipForm.addEventListener("submit", function (event) {
            if (ipAddress.value.trim() === "") {
                event.preventDefault();
                return;
            }
            loading.style.display = "block";
        });
    }

    // Card Animation on Page Load
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = "1";
            card.style.transform = "translateY(0.5)";
        }, index * 300);
    });

    // Function to Close the Popup
    window.closePopup = function() {
        successPopup.style.display = "none";
    };

    // Close Popup when clicking outside
    if (popupOverlay) {
        popupOverlay.addEventListener("click", function(event) {
            if (event.target === popupOverlay) {
                closePopup();
            }
        });
    }

    function revealCards() {
        serviceCards.forEach((card, index) => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;

            if (cardPosition < screenPosition) {
                setTimeout(() => {
                    card.classList.add("show");
                }, index * 200);
            }
        });
    }

    // Run animation when page loads
    revealCards();

    // Run animation on scroll
    window.addEventListener("scroll", revealCards);

    image.addEventListener("mouseover", () => {
        image.style.transform = "scale(1.05)";
        image.style.transition = "0.3s";
    });

    image.addEventListener("mouseout", () => {
        image.style.transform = "scale(1)";
    });

    image1.addEventListener("mouseover", () => {
        image1.style.transform = "scale(1.05)";
        image1.style.transition = "0.3s";
    });

    image1.addEventListener("mouseout", () => {
        image1.style.transform = "scale(1)";
    });

    teamCards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.style.transition = "0.3s ease-in-out";
        });

        card.addEventListener("mouseleave", () => {
            card.style.transition = "0.3s ease-in-out";
        });
    });
    passwordInput.addEventListener("input", function () {
        let password = passwordInput.value;
        let progress = 20;
        let color = "red";
        let strength = "Very Weak";

        if (password.length >= 8) progress = 40, color = "orange", strength = "Weak";
        if (/[A-Z]/.test(password)) progress = 60, color = "yellow", strength = "Moderate";
        if (/[0-9]/.test(password) && /[@$!%*?&#]/.test(password)) progress = 80, color = "blue", strength = "Strong";
        if (password.length > 12) progress = 100, color = "green", strength = "Very Strong";

        strengthText.textContent = strength;
        strengthText.style.color = color;
        progressBar.style.width = progress + "%";
        progressBar.style.backgroundColor = color;
    });
});
