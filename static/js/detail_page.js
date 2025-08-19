document.addEventListener('DOMContentLoaded', () => {
    const textContainer = document.querySelector('.text-container');
    const readMoreBtn = document.getElementById('read-more-btn');

    // 모바일 환경에서만 실행
    if (window.innerWidth <= 768) {
        readMoreBtn.addEventListener('click', () => {
            textContainer.classList.toggle('expanded');

            if (textContainer.classList.contains('expanded')) {
                readMoreBtn.textContent = 'Read less';
            } else {
                readMoreBtn.textContent = 'Read more';
            }
        });
    }
});