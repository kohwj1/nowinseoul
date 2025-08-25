document.addEventListener('DOMContentLoaded', function () {
//   read more
  const textContainer = document.querySelector('.text-container');
  const readMoreBtn = document.getElementById('read-more-btn');
  if (textContainer && readMoreBtn) {
    readMoreBtn.addEventListener('click', () => {
      textContainer.classList.toggle('expanded');
      readMoreBtn.textContent = textContainer.classList.contains('expanded') ? 'Read less' : 'Read more';
    });
  }
//   따릉이 합
  const totalBikesHeader = document.getElementById('total-bikes');
  if (totalBikesHeader && Array.isArray(bikeData) && bikeData.length > 0) {
    const total = bikeData.reduce((s, st) => s + (parseInt(st.SBIKE_PARKING_CNT, 10) || 0), 0);
    totalBikesHeader.textContent = `${total} Public bike(s) available`;
  }
});
