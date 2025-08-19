document.addEventListener('DOMContentLoaded', () => {
    const textContainer = document.querySelector('.text-container');
    const readMoreBtn = document.getElementById('read-more-btn');
    const locationDescription = document.getElementById('location-description');

    // 모바일 환경에서만 실행
    if (window.innerWidth <= 768) {
        // 텍스트가 컨테이너 높이보다 길 때만 버튼 표시
        if (locationDescription.offsetHeight > textContainer.clientHeight) {
            readMoreBtn.style.display = 'block';
        } else {
            readMoreBtn.style.display = 'none';
        }

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