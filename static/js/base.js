document.querySelectorAll('.messages .alert').forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = 0;
        setTimeout(() => {
            alert.style.display = 'none';
        }, 500);
    }, 5000);
});