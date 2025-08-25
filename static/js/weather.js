document.addEventListener('DOMContentLoaded', function () {
    // weather
  const firstTime = document.querySelector('.forecast-item .time');
  if (firstTime) firstTime.textContent = 'Now';

  if (typeof pageData !== 'undefined' && Array.isArray(pageData.WEATHER_STTS)) {
    const weatherData = pageData.WEATHER_STTS;
    const forecastItems = document.querySelectorAll('.forecast-item');

    forecastItems.forEach((item, idx) => {
      const data = weatherData[idx];
      if (!data) return;

      const rainChance = parseInt(data.RAIN_CHANCE, 10);
      const graph = item.querySelector('.rain-chance-graph');
      if (!graph) return;

      const height = isNaN(rainChance) ? 0 : Math.max(0, rainChance);
      graph.style.setProperty('--rain-height', `${height}%`);
    });
  }

  //   날씨 좌우 스크롤
  const scroller = document.querySelector('.weather-forecast-container');
  const leftBtn = document.querySelector('.weather-scroll-controls .scroll-btn.left');
  const rightBtn = document.querySelector('.weather-scroll-controls .scroll-btn.right');
  const progBar = document.querySelector('.weather-scroll-controls .scroll-progress-bar');

  if (scroller && leftBtn && rightBtn && progBar) {
    const scrollStep = () => Math.max(240, Math.floor(scroller.clientWidth * 0.8)); // 80% or 240px

    const updateEdgeAndProgress = () => {
      const max = scroller.scrollWidth - scroller.clientWidth;
      const x = Math.max(0, Math.min(scroller.scrollLeft, max));
      const pct = max <= 0 ? 100 : Math.round((x / max) * 100);
      progBar.style.width = `${pct}%`;
      leftBtn.disabled = x <= 2;
      rightBtn.disabled = x >= max - 2;
    };

    leftBtn.addEventListener('click', () => {
      scroller.scrollBy({ left: -scrollStep(), behavior: 'smooth' });
    });
    rightBtn.addEventListener('click', () => {
      scroller.scrollBy({ left: scrollStep(), behavior: 'smooth' });
    });
    scroller.addEventListener('scroll', updateEdgeAndProgress);
    window.addEventListener('resize', updateEdgeAndProgress);

    setTimeout(updateEdgeAndProgress, 0);
  }
});