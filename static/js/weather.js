document.addEventListener("DOMContentLoaded", () => {
  const forecastContainer = document.querySelector(".weather-forecast");
  const tempEls = document.querySelectorAll(".weather-forecast .forecast-item .temp");
  const headerTempEl = document.querySelector(".weather-header .current-temp");
  const unitBtns = document.querySelectorAll(".unit-btn");

  // 원본 섭씨 배열 확보
  let cTemps = [];
  if (window.pageData?.WEATHER_STTS?.length) {
    cTemps = window.pageData.WEATHER_STTS.map(x => parseFloat(String(x?.TEMP)));
  } else if (tempEls.length) {
    cTemps = Array.from(tempEls).map(el => parseFloat(el.textContent));
  }

  const toF = c => c * 9 / 5 + 32;
  const fmt = n => Number.isFinite(n) ? Math.round(n) : "--";
  const normalizeUnit = u => (u ? String(u).toUpperCase() : "C"); 

  function render(rawUnit) {
    const unit = normalizeUnit(rawUnit);

    if (headerTempEl && cTemps.length) {
      const base = cTemps[0];
      const val = unit === "F" ? toF(base) : base;
      headerTempEl.innerHTML = `${fmt(val)}<span class="unit">°${unit}</span>`;
    }

    tempEls.forEach((el, idx) => {
      const c = cTemps[idx];
      const val = unit === "F" ? toF(c) : c;
      el.innerHTML = `${fmt(val)}<span class="unit">°${unit}</span>`;
    });

    unitBtns.forEach(b => b.classList.toggle("active", normalizeUnit(b.dataset.unit) === unit));

    try { localStorage.setItem("tempUnit", unit); } catch (e) {}
  }

  // 버튼 클릭 이벤트 (단위 정규화)
  unitBtns.forEach(btn => {
    btn.addEventListener("click", () => render(btn.dataset.unit));
  });

  // 초기 단위 (로컬스토리지 값 정규화)
  let initial = "C";
  try {
    const saved = localStorage.getItem("tempUnit");
    const norm = normalizeUnit(saved);
    if (norm === "F" || norm === "C") initial = norm;
  } catch (e) {}

  render(initial);

  // 스크롤 트랙 클릭 스크롤 유지
  const scrollTrack = document.querySelector(".scroll-track");
  if (scrollTrack && forecastContainer) {
    const updateMax = () => forecastContainer.scrollWidth - forecastContainer.clientWidth;
    scrollTrack.addEventListener("click", (e) => {
      const rect = scrollTrack.getBoundingClientRect();
      const ratio = Math.min(Math.max((e.clientX - rect.left) / rect.width, 0), 1);
      forecastContainer.scrollLeft = updateMax() * ratio;
    });
  }
});
