document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    const paginationContainer = document.querySelector('.pagination-container');
    const pageNumbersDiv = document.getElementById('page-numbers');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    //6개 제한
    const itemsPerPage = 6; 
    let currentPage = 1;
    const totalPages = Math.ceil(cards.length / itemsPerPage);

    function displayPage(page) {
        cards.forEach(card => {
            card.style.display = 'none';
        });

        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        for (let i = start; i < end && i < cards.length; i++) {
            cards[i].style.display = 'block';
        }
    }

    function setupPagination() {
        // 페이지 번호 
        pageNumbersDiv.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const pageLink = document.createElement('a');
            pageLink.href = '#';
            pageLink.textContent = i;
            pageLink.classList.add('page-link');
            if (i === currentPage) {
                pageLink.classList.add('active');
            }
            pageLink.addEventListener('click', (e) => {
                e.preventDefault();
                currentPage = i;
                updatePagination();
            });
            pageNumbersDiv.appendChild(pageLink);
        }
    }

    function updatePagination() {
        displayPage(currentPage);
        setupPagination();

        //prev, next 비활성화
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
    }

    prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });

    //초기화
    updatePagination();
});