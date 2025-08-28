function initPage() {
  // --- read more ---
  const textContainer = document.querySelector('.text-container');
  const readMoreBtn = document.getElementById('read-more-btn');
  if (textContainer && readMoreBtn) {
    readMoreBtn.addEventListener('click', () => {
      textContainer.classList.toggle('expanded');
      readMoreBtn.textContent = textContainer.classList.contains('expanded')
        ? 'Read less'
        : 'Read more';
    });
  }

  // --- 따릉이 합 ---
  const totalBikesHeader = document.getElementById('total-bikes');
  if (totalBikesHeader && Array.isArray(bikeData) && bikeData.length > 0) {
    const total = bikeData.reduce((s, st) => s + (parseInt(st.SBIKE_PARKING_CNT, 10) || 0), 0);
    totalBikesHeader.textContent = `${total} Public bike(s) available`;
  }
}

// 최초 로드 시 실행
document.addEventListener('DOMContentLoaded', initPage);

// 뒤로가기 등 BFCache 복원 시 실행
window.addEventListener('pageshow', (e) => {
  if (e.persisted) {
    initPage();
  }
});

// --- 뒤로 가기 버튼 ---
function goBack() {
  if (document.referrer !== "") {
    history.back();
  } else {
    window.location.href = "{{ url_for('index') }}"; // 메인으로 이동
  }
}
