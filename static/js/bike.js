//따릉이용 서클 마커
function circleOnMap(marker_data, map) {
    try {
        for (m of marker_data) {
            if (m.SBIKE_PARKING_CNT != 0) {
                L.marker([m.SBIKE_X, m.SBIKE_Y], {icon: L.icon({
                    iconUrl: '../../static/images/ui/marker_bicycle.png',
                    iconSize: [30, 36],
                    iconAnchor: [22, 15],
                    popupAnchor: [-7, 2]
                })})
                .bindPopup(`<strong>${m.SBIKE_SPOT_NM}</strong><br><br>${m.SBIKE_PARKING_CNT}${translateBike(userLocale)}`)
                .addTo(map)
                L.marker([m.SBIKE_X, m.SBIKE_Y],{icon: L.divIcon({html: `<div class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">${m.SBIKE_PARKING_CNT}</div>`, iconSize: [0, 0], iconAnchor: [-10, 12],})})
                .addTo(map)
        } else {
            L.marker([m.SBIKE_X, m.SBIKE_Y], {icon: L.icon({
                    iconUrl: '../../static/images/ui/marker_no_bicycle.png',
                    iconSize: [30, 36],
                    iconAnchor: [22, 15],
                    popupAnchor: [-7, 2]
                })})
                .bindPopup(`<strong>${m.SBIKE_SPOT_NM}</strong><br><br>${m.SBIKE_PARKING_CNT}${translateBike(userLocale)}`)
                .addTo(map)
                L.marker([m.SBIKE_X, m.SBIKE_Y],{icon: L.divIcon({html: `<div class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-secondary">${m.SBIKE_PARKING_CNT}</div>`, iconSize: [0, 0], iconAnchor: [-10, 12],})})
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
            maxZoom: 19,
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