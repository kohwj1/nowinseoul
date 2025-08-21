
//따릉이용 마커
function circleOnMap(marker_data, map) {
    try {
        for (m of marker_data.SBIKE_STTS) {
            if (m.SBIKE_PARKING_CNT != 0) {
                L.circleMarker([m.SBIKE_X, m.SBIKE_Y], {radius: 15, color: '#33a758', fillColor: '#33a758', fillOpacity: 1})
                .addTo(map)
                L.marker([m.SBIKE_X, m.SBIKE_Y],{icon: L.divIcon({html: `<div class="circle-text">${m.SBIKE_PARKING_CNT}</div>`, iconSize: [0, 0], iconAnchor: [6, 11],})})
                .bindPopup(`<strong>${m.SBIKE_SPOT_NM}</strong><br><br>${m.SBIKE_PARKING_CNT} bike(s)`)
                .addTo(map)
        }
    }
    } catch {
        return;   
    }
}


document.addEventListener('DOMContentLoaded', () => {
    //지도 렌더링
    try{
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
    } catch {
        let map = L.map('map', {
            center: [37.5665, 126.9780],
            zoom: 16,
        });
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 17,
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
        circleOnMap(bike_list, map)
    }

})