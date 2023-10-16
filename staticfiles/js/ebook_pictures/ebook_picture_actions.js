document.addEventListener("DOMContentLoaded", function() {
    // Select all "More" buttons
    const buttons = document.querySelectorAll('.card button');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Navigate to the URL stored in the data-url attribute
            window.location.href = button.getAttribute('data-url');
        });
    });
});
