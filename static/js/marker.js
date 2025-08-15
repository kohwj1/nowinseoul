//커스텀 마커
function customMarker(crowdLevel) {
    switch(crowdLevel) {
        case 'Low Density':
            iconUrl = 'static/img/marker_0.png'
            break;
        case 'Medium Density':
            iconUrl = 'static/img/marker_1.png'
            break;
        case 'Slightly Crowded':
            iconUrl = 'static/img/marker_2.png'
            break;
        case 'Crowded':
            iconUrl = 'static/img/marker_3.png'
            break;
    }
    const marker = L.icon({
        iconUrl: iconUrl,
        iconSize: [46, 54],
        iconAnchor: [22, 94],
        popupAnchor: [0, -76] 
    });
    return marker
}

//맵에 마킹
function markOnMap(marker_data) {

    //기존 마커 모두 제거
    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    for (m of marker_data) {
        L.marker([m.lat, m.lng], {icon: customMarker(m.crowd)})
        .bindPopup(`<strong>${m.name}</strong><br>${m.crowd}<br><br><a href="/detail/${m.id}">&gt;&gt; Go to Detail</a>`)
        .addTo(map)
    }
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