//따릉이용 서클 마커
function circleOnMap(marker_data, map) {
    try {
        for (m of marker_data) {
            if (m.SBIKE_PARKING_CNT != 0) {
                L.circleMarker([m.SBIKE_X, m.SBIKE_Y], {radius: 15, color: '#33a758', fillColor: '#33a758', fillOpacity: 1})
                .addTo(map)
                L.marker([m.SBIKE_X, m.SBIKE_Y],{icon: L.divIcon({html: `<div class="circle-text">${m.SBIKE_PARKING_CNT}</div>`, iconSize: [0, 0], iconAnchor: [0, 0],})})
                .bindPopup(`<strong>${m.SBIKE_SPOT_NM}</strong><br><br>${m.SBIKE_PARKING_CNT} bike(s)`)
                .addTo(map)
        }
    }
    } catch {
        console.log('서버 데이터 확인 필요')
        return;   
    }
}

document.addEventListener('DOMContentLoaded', () => {
    //지도 렌더링
    try{
        const initLat = bikeData[0].SBIKE_X;
        const initLng = bikeData[0].SBIKE_Y;
        console.log(initLat, initLng);
        
        let map = L.map('map', {
            center: [initLat, initLng],
            zoom: 16,
        });
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 17,
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
        circleOnMap(bikeData, map)
    } catch {
        const msgNoBike = document.createElement('div')
        msgNoBike.textContent = 'No bike available'
        msgNoBike.classList.add('no-bike')
        document.getElementById('map').appendChild(msgNoBike)
    }
})