document.addEventListener('DOMContentLoaded', function(){
  // 1) 강수 그래프에 데이터 반영
  try {
    const wd = window.pageData?.WEATHER_STTS || window.weatherData || [];
    const items = document.querySelectorAll('.weather-forecast .forecast-item');

    items.forEach((el, idx) => {
      const data = wd[idx];
      const bar = el.querySelector('.rain-chance-graph');
      const pct = el.querySelector('.rain-chance');
      if (!data || !bar) return;

      // 0~100 보정
      const val = Math.max(0, Math.min(100, Number(data.RAIN_CHANCE) || 0));
      bar.style.setProperty('--rain-height', `${val}%`);
      if (pct) pct.textContent = `${val}%`;

      // (선택) 온도/시간도 서버 렌더가 비었으면 채우기
      const tempEl = el.querySelector('.temp');
      if (tempEl && tempEl.textContent.trim() === '') {
        const t = data.TEMP != null ? String(data.TEMP) : '--';
        tempEl.innerHTML = `${t}<span class="unit">°C</span>`;
      }
      const timeEl = el.querySelector('.time');
      if (timeEl && timeEl.textContent.trim() === '') {
        // data.FCST_DT 가 'YYYYMMDDHH' 또는 'YYYY-MM-DD HH:mm' 유형일 때 HH만 추출 시도
        const s = String(data.FCST_DT || '');
        const hh = s.match(/(\d{2})(?::?00)?$/)?.[1] || '--';
        timeEl.textContent = `${hh}:00`;
      }
    });

    // 2) 현재온도(헤더)도 첫 항목 기준으로 갱신(서버 렌더와 불일치 대비)
    const headerTemp = document.querySelector('.weather-header .current-temp');
    if (headerTemp && wd[0] && wd[0].TEMP != null) {
      headerTemp.innerHTML = `${wd[0].TEMP}<span class="unit">°C</span>`;
    }
  } catch (e) {
    console.warn('weather render error', e);
  }

  // 3) 썸 ↔ 컨테이너 스크롤 동기화
  const container = document.querySelector('.weather-forecast');
  const track = document.querySelector('.weather-scroll-controls .scroll-track');
  const thumb = document.querySelector('.weather-scroll-controls .scroll-thumb');
  if (!container || !track || !thumb) return;

  function clamp(v, min, max){ return v < min ? min : (v > max ? max : v); }

  function syncThumb(){
    const maxScroll = Math.max(0, container.scrollWidth - container.clientWidth);
    const ratio = maxScroll === 0 ? 0 : (container.scrollLeft / maxScroll);
    const trackW = track.clientWidth;
    const thumbW = thumb.offsetWidth;
    const x = ratio * (trackW - thumbW);
    thumb.style.left = `${x + thumbW/2}px`;     // translate(-50%) 기준
    track.setAttribute('aria-valuenow', Math.round(ratio*100));
  }

  let dragging = false, pid = null;

  function onPointerDown(e){
    dragging = true; pid = e.pointerId || null;
    thumb.setPointerCapture?.(pid);
    e.preventDefault();
  }

  function onPointerMove(e){
    if (!dragging) return;
    const rect = track.getBoundingClientRect();
    const thumbW = thumb.offsetWidth;
    const trackW = rect.width;

    let x = e.clientX - rect.left - thumbW/2;
    x = clamp(x, 0, trackW - thumbW);

    const ratio = (trackW - thumbW) === 0 ? 0 : x / (trackW - thumbW);
    const maxScroll = Math.max(0, container.scrollWidth - container.clientWidth);
    container.scrollLeft = ratio * maxScroll;

    // 즉시 썸 위치 반영
    thumb.style.left = `${x + thumbW/2}px`;
    track.setAttribute('aria-valuenow', Math.round(ratio*100));
    e.preventDefault();
  }

  function onPointerUp(){
    if (!dragging) return;
    dragging = false;
    if (pid != null) thumb.releasePointerCapture?.(pid);
    pid = null;
  }

  function onTrackClick(e){
    if (e.target === thumb) return;
    const rect = track.getBoundingClientRect();
    const thumbW = thumb.offsetWidth;
    const trackW = rect.width;
    let x = e.clientX - rect.left - thumbW/2;
    x = clamp(x, 0, trackW - thumbW);

    const ratio = (trackW - thumbW) === 0 ? 0 : x / (trackW - thumbW);
    const maxScroll = Math.max(0, container.scrollWidth - container.clientWidth);
    container.scrollLeft = ratio * maxScroll;
  }

  container.addEventListener('scroll', syncThumb, { passive:true });
  window.addEventListener('resize', syncThumb);

  thumb.addEventListener('pointerdown', onPointerDown);
  window.addEventListener('pointermove', onPointerMove, { passive:false });
  window.addEventListener('pointerup', onPointerUp);
  window.addEventListener('pointercancel', onPointerUp);

  track.addEventListener('click', onTrackClick);

  requestAnimationFrame(syncThumb);
})();

