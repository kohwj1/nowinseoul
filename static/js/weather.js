// weather.js  — 그래프 스타일 유지 버전 (DOM 재생성 없음)

document.addEventListener("DOMContentLoaded", () => {
  // 페이지에 이미 렌더된 예보 아이템들
  const forecastContainer = document.querySelector(".weather-forecast");
  const tempEls = document.querySelectorAll(".weather-forecast .forecast-item .temp");
  const headerTempEl = document.querySelector(".weather-header .current-temp");
  const unitBtns = document.querySelectorAll(".unit-btn");

  // 섭씨 원본 값 확보: 우선 서버 데이터, 없으면 DOM에서 파싱
  let cTemps = [];
  if (window.pageData?.WEATHER_STTS?.length) {
    cTemps = window.pageData.WEATHER_STTS.map(x => Number(x?.TEMP));
  } else if (tempEls.length) {
    cTemps = Array.from(tempEls).map(el => parseFloat(el.textContent));
  }

  function toF(c) { return c * 9 / 5 + 32; }
  function fmt(n) { return Number.isFinite(n) ? Math.round(n) : "--"; }

  function render(unit) {
    // 헤더 현재 온도: 첫 항목 기준
    if (headerTempEl && cTemps.length) {
      const base = cTemps[0];
      const val = unit === "F" ? toF(base) : base;
      headerTempEl.innerHTML = `${fmt(val)}<span class="unit">°${unit}</span>`;
    }

    // 예보 온도들 텍스트만 교체 (그래프/스타일 그대로)
    tempEls.forEach((el, idx) => {
      const c = cTemps[idx];
      const val = unit === "F" ? toF(c) : c;
      el.innerHTML = `${fmt(val)}<span class="unit">°${unit}</span>`;
    });

    // 토글 버튼 상태
    unitBtns.forEach(b => b.classList.toggle("active", b.dataset.unit === unit));

    // 저장
    try { localStorage.setItem("tempUnit", unit); } catch (e) {}
  }

  // 버튼 이벤트
  unitBtns.forEach(btn => {
    btn.addEventListener("click", () => render(btn.dataset.unit));
  });

  // 초기 단위
  let initial = "C";
  try {
    const saved = localStorage.getItem("tempUnit");
    if (saved === "F" || saved === "C") initial = saved;
  } catch (e) {}

  render(initial);

  // ===== 선택: 스크롤 트랙 클릭으로 예보 가로 스크롤 유지 =====
  const scrollTrack = document.querySelector(".scroll-track");
  if (scrollTrack && forecastContainer) {
    function updateMax() {
      return forecastContainer.scrollWidth - forecastContainer.clientWidth;
    }
    scrollTrack.addEventListener("click", (e) => {
      const rect = scrollTrack.getBoundingClientRect();
      const ratio = Math.min(Math.max((e.clientX - rect.left) / rect.width, 0), 1);
      forecastContainer.scrollLeft = updateMax() * ratio;
    });
  }
});
