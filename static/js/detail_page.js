document.addEventListener('DOMContentLoaded', () => {
    const textContainer = document.querySelector('.text-container');
    const readMoreBtn = document.getElementById('read-more-btn');

    // The event listener is now active for all screen sizes
    readMoreBtn.addEventListener('click', () => {
        textContainer.classList.toggle('expanded');

        if (textContainer.classList.contains('expanded')) {
            readMoreBtn.textContent = 'Read less';
        } else {
            readMoreBtn.textContent = 'Read more';
        }
    });
});