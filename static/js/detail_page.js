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

//   read more
  const textContainer = document.querySelector('.text-container');
  const readMoreBtn = document.getElementById('read-more-btn');
  if (textContainer && readMoreBtn) {
    readMoreBtn.addEventListener('click', () => {
      textContainer.classList.toggle('expanded');
      readMoreBtn.textContent = textContainer.classList.contains('expanded') ? 'Read less' : 'Read more';
    });
  }

//   crow density
(function renderCrowdBar() {
  const progressBar = document.getElementById('crowd-density-bar');
  const timeLabels = [
    document.getElementById('time-now'),
    document.getElementById('time-1'),
    document.getElementById('time-2'),
    document.getElementById('time-3')
  ];
  const badgeEl = document.querySelector('.crowd-density-section #traffic-tag');

  if (!progressBar || !timeLabels[0] || !Array.isArray(crowdData) || crowdData.length === 0) return;

  // "YYYY-MM-DD HH:mm"
  const toLocalDate = (s) => new Date(String(s).replace(' ', 'T'));
  const floorToHour = (d) => { const t = new Date(d); t.setMinutes(0,0,0); return t; };
  const fmtHHMM = (h) => String(h).padStart(2,'0') + ':00';

  const rows = crowdData
    .map(it => ({ dt: toLocalDate(it.FCST_TIME), lvl: it.FCST_CONGEST_LVL }))
    .filter(it => !isNaN(it.dt))
    .sort((a,b) => a.dt - b.dt);

  if (!rows.length) return;

  const now = new Date();
  const curHour = floorToHour(now);
  let startIdx = rows.findIndex(r => r.dt >= curHour);
  const usingFallback = startIdx === -1;
  if (usingFallback) startIdx = 0;

  const upcoming = rows.slice(startIdx, startIdx + 4);
  if (!upcoming.length) return;

  if (badgeEl) {
    const level = upcoming[0].lvl;               
    const cls = level === 'Comfortable' ? 'comfortable'
              : level === 'Moderate'    ? 'medium'
              : level === 'Crowded'     ? 'congested' : '';
    badgeEl.textContent = (level === 'Moderate') ? 'Medium' : level;
    badgeEl.classList.remove('comfortable','medium','congested');
    if (cls) badgeEl.classList.add(cls);
  }

    if (timeLabels[0]) {
    timeLabels[0].textContent = 'Now';
    }
  for (let i = 1; i < 4; i++) {
    if (!timeLabels[i]) continue;
    const row = upcoming[i];
    timeLabels[i].textContent = row ? fmtHHMM(row.dt.getHours()) : '--';
  }

  progressBar.innerHTML = '';
})();


//   따릉이 합
  const totalBikesHeader = document.getElementById('total-bikes');
  if (totalBikesHeader && Array.isArray(bikeData) && bikeData.length > 0) {
    const total = bikeData.reduce((s, st) => s + (parseInt(st.SBIKE_PARKING_CNT, 10) || 0), 0);
    totalBikesHeader.textContent = `${total} Public bike(s) available`;
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
