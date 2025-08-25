//검색 또는 필터 UI 조정 시 현재 상태값 가져오는 함수
function getFilterArgs() {
    const keyword = document.getElementById('mapSearch').value;
    const theme = Array.from(document.querySelectorAll('input[name="theme"]:checked')).map((t) => t.value);
    const crowd = document.querySelector('input[name="crowd"]:checked').value;
    // console.log(keyword, theme, crowd)
    return {keyword: keyword, theme: theme, crowd: crowd}
}

function placeFilter(keyword, theme, crowd) {
    let filtered_data = originMapData
    
    if (keyword !== '') {
        filtered_data = filtered_data.filter(place => place.name.toLowerCase().includes(keyword.toLowerCase()));
    }
    if (theme.includes('food')) {
        filtered_data = filtered_data.filter(place => place.food != 0);
    }
    if (theme.includes('drama')) {
        filtered_data = filtered_data.filter(place => place.drama != 0);
    }
    if (theme.includes('movie')) {
        filtered_data = filtered_data.filter(place => place.movie != 0);
    }
    if (theme.includes('beauty')) {
        filtered_data = filtered_data.filter(place => place.beauty != 0);
    }
    if (crowd !== 'all') {
        filtered_data = filtered_data.filter(place => place.crowd == crowd);
    }
    
    console.log(filtered_data)
    return filtered_data
}

function searchPlace() {
    const filter_agrs = getFilterArgs()
    const filtered_data = placeFilter(filter_agrs.keyword, filter_agrs.theme, filter_agrs.crowd)
    clearMap()
    markOnMap(filtered_data);
    heatOnMap(filtered_data);
    openTooltip();
}

//필터 UI 조작 시마다 마커 갱신
const filter_items = document.querySelectorAll('.mapfilter')
for (i of filter_items) {
    i.addEventListener('click', () => {
        const filter_agrs = getFilterArgs()
        const filtered_data = placeFilter(filter_agrs.keyword, filter_agrs.theme, filter_agrs.crowd)
        clearMap()
        markOnMap(filtered_data)
        heatOnMap(filtered_data)
    })
}

//filter UI 접기/펼치기

const windowwidth = window.innerWidth
let isFilterDisplayed = false;
const filterDisplayBtn = document.getElementById('filterDisplay');
const filterUI = document.getElementById('mapFilter');
const filterDiv = document.getElementById('filterDiv');
const filterBody = document.querySelector('#filterDiv .accordion-body');

filterDisplayBtn.addEventListener('click', () => {
    if (windowwidth <= 1000) {
        if (!isFilterDisplayed) {
            filterUI.style.bottom = '36px';
        } else {
            filterUI.style.bottom = 36 + -1 * filterBody.offsetHeight + 'px';
        }
        filterUI.classList.toggle('move-up');
        filterDisplayBtn.classList.toggle('collapsed')
        isFilterDisplayed = !isFilterDisplayed;
    }
});

document.addEventListener('DOMContentLoaded', () => {
    if (windowwidth <= 1000) {
        filterUI.style.bottom = 36 + -1 * filterBody.offsetHeight + 'px';
    }
    clearMap()
    markOnMap(originMapData)
    heatOnMap(originMapData)
    }
)

document.getElementById('btnReset').addEventListener('click', () => {
        clearMap()
        markOnMap(originMapData)
        heatOnMap(originMapData)
    }
)

document.getElementById('btnSearch').addEventListener('click', () => {
    const keyword = document.getElementById('mapSearch').value;
    if (keyword == '') {
        return;
    } else {
        searchPlace()
    }
})
document.getElementById('filterForm').addEventListener('submit', (e) => {
    e.preventDefault()
})