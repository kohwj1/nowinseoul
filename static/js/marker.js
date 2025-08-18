//커스텀 마커
function customMarker(crowdLevel) {
    const crowd_icon_url = {
        'Low Density':'static/images/marker_0.png', 
        'Medium Density':'static/images/marker_1.png', 
        'Slightly Crowded':'static/images/marker_2.png', 
        'Crowded':'static/images/marker_3.png', 
    }

    const marker = L.icon({
        // iconUrl: crowd_icon_url[crowdLevel],
        iconUrl: 'static/images/marker_none.png',
        iconSize: [30, 36],
        // iconAnchor: [22, 94],
        iconAnchor: [22, 15],
        // popupAnchor: [0, -76], 
        popupAnchor: [0, -5] 
    });
    return marker
}

//히트레벨 리턴 함수
function heatLevel(crowdLevel) {
    const crowd_level_value = {
        'Low Density': 0.25, 
        'Medium Density': 0.5, 
        'Slightly Crowded': 0.75, 
        'Crowded': 1, 
    }
    return crowd_level_value[crowdLevel]
}

function clearMap() {
    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker || layer instanceof L.HeatLayer) {
            map.removeLayer(layer);
        }
    });
}


//맵에 마킹
function markOnMap(marker_data) {
    for (m of marker_data) {
        L.marker([m.lat, m.lng], {icon: customMarker(m.crowd)})
        .bindPopup(`<strong>${m.name}</strong><br>${m.crowd}<br><br><a class="gotoDetail" href="/detail/${m.id}">&gt;&gt; Go to Detail</a>`)
        .addTo(map)
    }
}

function heatOnMap(marker_data) {
    let heatData = []

    for (m of marker_data) {
        heatData.push([m.lat, m.lng, heatLevel(m.crowd)])
    }

    L.heatLayer(heatData, {
        radius: 30,
        blur: 24,
        maxZoom: 17,
        gradient: {
            0.25: 'blue',
            0.5: 'lime',
            0.75: 'orange',
            1.0: 'red'
        }
    })
    .addTo(map);
}


//검색어 입력 시 맵 중앙 자동이동 및 팝업 오픈
function openTooltip() {
    map.eachLayer(function(layer) {
    if (layer instanceof L.Marker) {
        map.get
        map.setView(layer.getLatLng());
        layer.openPopup();
        return;
        }
    });
}

//지도 렌더링
let map = L.map('map', {
    center: [37.5665, 126.9780],
    zoom: 17,
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);