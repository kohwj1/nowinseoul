document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('tagForm');
  const endpoint = form?.dataset?.endpoint || '/main-feature';
  const checkboxes = Array.from(document.querySelectorAll('.mapfilter'));
  const grid = document.getElementById('cardGrid');
  const emptyState = document.getElementById('emptyState');
  const loadingState = document.getElementById('loadingState');

  const makeCardHtml = (item) => {
    const detailHref = `/detail/${encodeURIComponent(item.id)}`;
    const imgSrc = `../static/images/attraction/${encodeURIComponent(item.id)}.jpg`;
    const title = item.name || '';
    return `
      <div class="card">
        <a href="${detailHref}">
          <img src="${imgSrc}" alt="main image" class="card-image" />
          <div class="card-title">${escapeHtml(title)}</div>
        </a>
      </div>
    `;
  };

  const escapeHtml = (str) => String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');

  const setLoading = (on) => {
    if (!loadingState) return;
    loadingState.style.display = on ? 'block' : 'none';
  };
  const setEmpty = (on) => {
    if (!emptyState) return;
    emptyState.style.display = on ? 'block' : 'none';
  };

  const renderCards = (items) => {
    if (!grid) return;
    if (!items || items.length === 0) {
      grid.innerHTML = '';
      setEmpty(true);
      return;
    }
    setEmpty(false);
    grid.innerHTML = items.map(makeCardHtml).join('');
  };

  const fetchFiltered = async (selected) => {
    const tags = selected.join(',');
    const body = `tags=${encodeURIComponent(tags)}`;

    setLoading(true);
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const json = await res.json();
      // 기대 응답 형태: { tags: "Food,Drama", data: [{id, name}, ...] }
      const items = json?.data || [];
      renderCards(items);
    } catch (err) {
      console.error('태그 필터 요청 실패:', err);
      // 실패 시 UX: 기존 카드 유지 + 토스트/알림을 원하시면 여기서 추가
      alert('필터 데이터를 불러오지 못했어요. 잠시 후 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  // 디바운스 (체크 여러 개 빠르게 눌러도 호출 1회로)
  let debounceTimer = null;
  const triggerFetch = () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const selected = checkboxes
        .filter(cb => cb.checked)
        .map(cb => cb.value.trim())
        .filter(Boolean);
      // 아무 것도 선택 안하면 전체 목록(빈 문자열)로 요청
      fetchFiltered(selected);
    }, 120);
  };

  // 이벤트 바인딩
  checkboxes.forEach(cb => cb.addEventListener('change', triggerFetch));
});
