const progressBar = document.getElementById('crowd-density-bar');
const label_area = document.querySelector('.time-labels');
const badgeEl = document.querySelector('#crowd-tag');
const originCrowdLevel = badgeEl.innerText;

function colorMap(level) {
  switch(level) {
    case 'Comfortable':
      return '#22c55e'
    case 'Moderate':
      return '#facc15';
    case 'Slightly crowded':
      return '#f97316';
    case 'Crowded':
      return '#ef4444';
    default:
      return '#a3a3a3';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // --- Crowd Density ---
    if (originCrowdLevel) {
      const displayLevel = translateCrowd(userLocale(), originCrowdLevel);
      badgeEl.textContent = displayLevel;
    };
    const softStops = [colorMap(originCrowdLevel)];

    if (crowdData.length !== 0) {
      crowdData.forEach((item, index) => {
        softStops.push(colorMap(item.FCST_CONGEST_LVL));
        const new_label = document.createElement('span');
        new_label.classList.add('crowd-label', 'label-hide');
  
        if (index % 4 == 3) {
          new_label.classList.remove('label-hide');
        }
  
        new_label.textContent = item.FCST_TIME.split(' ')[1];
        label_area.appendChild(new_label);
      })
      progressBar.style.background = `linear-gradient(to right, ${softStops.join(', ')})`;
    }
});
