document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.message').forEach(function(button) {
        button.addEventListener('click', function() {
            this.closest('.message').style.display = 'none';
        });
    });
});