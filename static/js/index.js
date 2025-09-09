// const langSelectBox = document.getElementById('lang-select');

// function userLocale() {
//     const url = new URL(window.location.href);
//     const pathName = url.pathname;
//     const pathSegments = pathName.split('/');
//     console.log(pathSegments)

//     if (pathSegments.length === 0) {
//         return 'en'
//     }
//     return pathSegments[1];
// }


document.addEventListener('DOMContentLoaded', function() {
  // const locale = userLocale()
  // console.log(locale)
  const checkboxes = document.querySelectorAll('.mapfilter');
  const container  = document.getElementById('attractions-container');
  // document.getElementById(locale).setAttribute('selected','');

  const attractionData = window.attractionData || {};

  // (초기/전체해제 시 사용) 지금은 movie이지만 나중에 가장 높은 검색량을 나타내는 변수가 생기면 그것과 교체 
  const DEFAULT_TAG = 'food_beauty_drama_movie';

  // 백엔드가 조합 키를 만들 때 쓴 기준 순서 
  const BACKEND_ORDER = ['food', 'beauty', 'drama', 'movie'];
  
  renderList(attractionData[DEFAULT_TAG] || []);

  // 체크박스 변경 이벤트
  checkboxes.forEach(cb => cb.addEventListener('change', updateBySelection));

  function updateBySelection() {
    const selected = Array.from(checkboxes)
      .filter(el => el.checked)
      .map(el => String(el.value || '').toLowerCase());

    if (selected.length === 0) {
      renderList(attractionData[DEFAULT_TAG] || []);
      return;
    }

    // 백엔드 순서에 맞춰 정렬 그리고 조합기 생성
    selected.sort((a, b) => BACKEND_ORDER.indexOf(a) - BACKEND_ORDER.indexOf(b));
    const key = selected.join('_');

    renderList(attractionData[key] || []);
  }

  function renderList(items) {
    if (!Array.isArray(items) || items.length === 0) {
      container.innerHTML = `<div class="empty">결과가 없습니다.</div>`;
      return;
    }

    const html = items.map(item => {
      const id   = item.id || item['id'];
      const name = item.name || item['name'];
      return `
        <div class="card">
          <a href="detail/${encodeURIComponent(id)}">
            <div>
              <img src="/static/images/attraction/${encodeURIComponent(id)}.webp" alt="${escapeHtml(name)}" class="card-image" />
              <div class="shadow-overlay"></div>
            </div>
            <div class="card-title">${escapeHtml(name)}</div>
          </a>
        </div>
      `;
    }).join('');

    container.innerHTML = html;
  }

  function escapeHtml(str) {
    return String(str)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }
});

langSelectBox.addEventListener('change', () => {
  const newLang = langSelectBox.value;
  console.log(newLang)
  location.href = `/${newLang}`
})