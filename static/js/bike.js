
//따릉이용 마커
function circleOnMap(marker_data, map) {
    for (m of marker_data.SBIKE_STTS) {
        if (m.SBIKE_PARKING_CNT != 0) {
            L.circleMarker([m.SBIKE_X, m.SBIKE_Y], {radius: 15, color: 'green', fillColor: 'green', fillOpacity: 0.5})
            .bindPopup(`<strong>${m.SBIKE_SPOT_NM}</strong><br>${m.SBIKE_PARKING_CNT}`)
            .addTo(map)
            L.marker([m.SBIKE_X, m.SBIKE_Y],{icon: L.divIcon({html: `<div class="circle-text">${m.SBIKE_PARKING_CNT}</div>`, iconSize: [0, 0], iconAnchor: [-1, 9],})})
            .addTo(map)
    }
}}


document.addEventListener('DOMContentLoaded', () => {
    //지도 렌더링
    const init_lat = bike_list.SBIKE_STTS[0].SBIKE_X;
    const init_lng = bike_list.SBIKE_STTS[0].SBIKE_Y;
    
    console.log(init_lat, init_lng);
    
    let map = L.map('map', {
        center: [init_lat, init_lng],
        zoom: 16,
    });
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 17,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    circleOnMap(bike_list, map)
})