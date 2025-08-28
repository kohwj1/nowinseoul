document.addEventListener('DOMContentLoaded', () => {
  const tagEl = document.querySelector('.traffic-conditions-section .info-tag');
  const road = Array.isArray(window.pageData?.ROAD_TRAFFIC_STTS)
    ? window.pageData.ROAD_TRAFFIC_STTS[0] : null;

  let raw = (road && (road.ROAD_TRAFFIC_IDX ?? road.road_traffic_idx)) 
            || (tagEl ? tagEl.textContent.trim() : '');

  const MAP = {
    '원활':      { en: 'Free Flow',  cls: 'free' },
    '서행':      { en: 'Slow',       cls: 'slow' },
    '정체':      { en: 'Congested',  cls: 'tcongested' },
    'FREE':      { en: 'Free Flow',  cls: 'free' },
    'FREE FLOW': { en: 'Free Flow',  cls: 'free' },
    'SLOW':      { en: 'Slow',       cls: 'slow' },
    'CONGESTED': { en: 'Congested',  cls: 'tcongested' }
  };

  const key = (raw || '').toString().trim().toUpperCase();
  const hit = MAP[key] || MAP[raw] || null;

  if (tagEl) {
    // 혹시 붙어있을 수 있는 상태 클래스들 제거
    tagEl.classList.remove('free','slow','tcongested','comfortable','medium','slightly','congested','tag-free','tag-slow','tag-congested');

    if (hit) {
      tagEl.textContent = hit.en;
      tagEl.classList.add(hit.cls); // free / slow / tcongested
    } else {
      tagEl.textContent = 'No Data';
    }
  }
});