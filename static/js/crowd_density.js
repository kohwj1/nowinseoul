document.addEventListener('DOMContentLoaded', function () {
  // --- Crowd Density ---
  (function renderCrowdBar() {
    const progressBar = document.getElementById('crowd-density-bar');
    const timeLabels = [
      document.getElementById('time-now'),
      document.getElementById('time-1'),
      document.getElementById('time-2'),
      document.getElementById('time-3')
    ];
    const badgeEl = document.querySelector(
      '.crowd-density-section .info-tag, .crowd-density-section #crowd-tag, .crowd-density-section #traffic-tag'
    );

    if (!progressBar || !timeLabels[0] || !Array.isArray(crowdData) || crowdData.length === 0) return;

    const toLocalDate = (s) => new Date(String(s).replace(' ', 'T')); // "YYYY-MM-DD HH:mm"
    const floorToHour = (d) => { const t = new Date(d); t.setMinutes(0,0,0); return t; };
    const hhmm = (d) => String(d.getHours()).padStart(2,'0') + ':00';

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

    const window = rows.slice(startIdx, startIdx + 4);  
    if (!window.length) return;

    const level = window[0].lvl;

    // --- 뱃지 텍스트 변환 ---
    const levelText = (level === 'Moderate') ? 'Medium'
                     : (level === 'Slightly crowded') ? 'Slightly Crowded'
                     : level;

    // --- CSS 클래스 매핑 ---
    const cls = level === 'Comfortable'      ? 'comfortable'
              : level === 'Moderate'         ? 'medium'
              : level === 'Slightly crowded' ? 'slightly'
              : level === 'Crowded'          ? 'congested'
              : '';

    if (badgeEl) {
      badgeEl.textContent = levelText;
      badgeEl.classList && badgeEl.classList.remove('comfortable','medium','slightly','congested');
      if (cls && badgeEl.classList) badgeEl.classList.add(cls);
    }

    if (timeLabels[0]) {
      timeLabels[0].textContent = usingFallback ? hhmm(window[0].dt) : 'Now';
    }
    for (let i = 1; i < 4; i++) {
      timeLabels[i].textContent = window[i] ? hhmm(window[i].dt) : '--';
    }

    // --- 색상 매핑 ---
    const colorOf = (lvl) => (
      lvl === 'Comfortable'      ? '#22c55e' : // 초록
      lvl === 'Moderate'         ? '#facc15' : // 노랑
      lvl === 'Slightly crowded' ? '#f97316' : // 주황
      lvl === 'Crowded'          ? '#ef4444' : // 빨강
                                  '#a3a3a3'   // 기본 회색
    );

    const n = window.length;
    const step = 100 / n;
    const softStops = [];

    window.forEach((r, i) => {
      const c = colorOf(r.lvl);
      const from = Math.round(i * step);
      const to   = Math.round((i + 1) * step);

      softStops.push(`${c} ${from}%`);

      if (i < n - 1) {
          const nextColor = colorOf(window[i+1].lvl);
          softStops.push(`${c} ${to-1}%`);
          softStops.push(`${nextColor} ${to+1}%`);
      }

      if (i === n - 1) softStops.push(`${c} ${to}%`);
    });

    progressBar.style.background = `linear-gradient(to right, ${softStops.join(', ')})`;
    progressBar.innerHTML = ''; 
  })();
});
