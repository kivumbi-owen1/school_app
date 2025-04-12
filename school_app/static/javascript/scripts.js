    // Remove flash messages after animation completes
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            const flashMessages = document.querySelectorAll('.flash-message');
            flashMessages.forEach(message => {
                message.addEventListener('animationend', function() {
                    if (message.style.opacity === '0') {
                        message.remove();
                    }
                });
            });
        }, 5000);
    });