document.addEventListener('DOMContentLoaded', function() {
    // Get the current URL path
    const currentPath = window.location.pathname;

    // Select all navigation links
    const navLinks = document.querySelectorAll('nav a');

    // Checks to see if the url path is defaulted ('/')
    // If true the 'Home' nav tab is added to the 'active' class
    if( currentPath === '/') {
        navLinks.item(0).classList.add('active');
    }

    // Loop through each navigation link
    navLinks.forEach(link => {
        // Check if the link's href matches the current path
        if (link.getAttribute('href') === currentPath) {
            // Add the 'active' class to the matching link
            link.classList.add('active');
        }
    });
});