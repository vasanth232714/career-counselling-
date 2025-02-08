// Toggle menu on mobile
function showMenu() {
    document.getElementById("navLinks").style.right = "0"; // Show menu
}

function hideMenu() {
    document.getElementById("navLinks").style.right = "-200px"; // Hide menu
}

// Optional: Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth' // Smooth scrolling animation
        });
    });
});
