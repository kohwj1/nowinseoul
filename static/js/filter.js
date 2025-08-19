//테스트용 더미 데이터 (나중에 서버에서 받아올 부분)
const origin_data = [
    {
        "id":"P12312",
        "name":"Gwanghwamun",
        "crowd":"Slightly Crowded",
        "lat":37.5662,
        "lng":126.9772,
        "food": 1,
        "drama": 1,
        "beauty": 1,
        "movie": 1,
    },
    {
        "id":"P12316",
        "name":"Gwangjang Market",
        "crowd":"Slightly Crowded",
        "lat":37.5662,
        "lng":126.9783,
        "food": 1,
        "drama": 0,
        "beauty": 0,
        "movie": 0,
    },
    {
        "id":"P12313",
        "name":"Cheonggyecheon",
        "crowd":"Crowded",
        "lat":37.5660,
        "lng":126.9779,
        "food": 0,
        "drama": 1,
        "beauty": 0,
        "movie": 1,
    },
    {
        "id":"P12314",
        "name":"Bosingak",
        "crowd":"Low Density",
        "lat":37.5664,
        "lng":126.9781,
        "food": 0,
        "drama": 1,
        "beauty": 0,
        "movie": 0,
    },
    {
        "id":"P12315",
        "name":"Jongno-5ga",
        "crowd":"Medium Density",
        "lat":37.5670,
        "lng":126.9779,
        "food": 0,
        "drama": 1,
        "beauty": 0,
        "movie": 0
    },
    {
        "id":"P12315",
        "name":"Jongno-3ga",
        "crowd":"Crowded",
        "lat":37.5685,
        "lng":126.9779,
        "food": 0,
        "drama": 1,
        "beauty": 0,
        "movie": 1
    },
    {
        "id":"P12315",
        "name":"Jonggak",
        "crowd":"Crowded",
        "lat":37.5672,
        "lng":126.9781,
        "food": 0,
        "drama": 1,
        "beauty": 0,
        "movie": 1
    },
]

//검색 또는 필터 UI 조정 시 현재 상태값 가져오는 함수
function getFilterArgs() {
    const keyword = document.getElementById('mapSearch').value;
    const theme = Array.from(document.querySelectorAll('input[name="theme"]:checked')).map((t) => t.value);
    const crowd = document.querySelector('input[name="crowd"]:checked').value;
    // console.log(keyword, theme, crowd)
    return {keyword: keyword, theme: theme, crowd: crowd}
}

function placeFilter(keyword, theme, crowd) {
    let filtered_data = origin_data
    
    if (keyword !== '') {
        filtered_data = filtered_data.filter(place => place.name.toLowerCase().includes(keyword.toLowerCase()));
    }
    if (theme.includes('food')) {
        filtered_data = filtered_data.filter(place => place.food == 1);
    }
    if (theme.includes('drama')) {
        filtered_data = filtered_data.filter(place => place.drama == 1);
    }
    if (theme.includes('movie')) {
        filtered_data = filtered_data.filter(place => place.movie == 1);
    }
    if (theme.includes('beauty')) {
        filtered_data = filtered_data.filter(place => place.beauty == 1);
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
let isFilterDisplayed = false;
const filterDisplayBtn = document.getElementById('filterDisplay');
const filterUI = document.getElementById('mapFilter');
const filterDiv = document.getElementById('filterDiv');
const filterBody = document.querySelector('#filterDiv .accordion-body');

filterDisplayBtn.addEventListener('click', () => {
    if (!isFilterDisplayed) {
        const bodyHeight = filterBody.offsetHeight;
        filterUI.style.bottom = bodyHeight + 'px';
    } else {
        filterUI.style.bottom = '0px';
    }
    filterUI.classList.toggle('move-up');
    isFilterDisplayed = !isFilterDisplayed;
});

document.addEventListener('DOMContentLoaded', () => {
        clearMap()
        markOnMap(origin_data)
        heatOnMap(origin_data)
    }
)
document.getElementById('btnReset').addEventListener('click', () => {
        clearMap()
        markOnMap(origin_data)
        heatOnMap(origin_data)
    }
)
document.getElementById('btnSearch').addEventListener('click', () => searchPlace())
document.getElementById('filterForm').addEventListener('submit', (e) => {
    e.preventDefault()
})