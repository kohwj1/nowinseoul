//따릉이용 서클 마커
const PageLocale = userLocale()

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
                .bindPopup(`<strong>${m.SBIKE_SPOT_NM}</strong><br><br><div class="bike-count-bubble">${m.SBIKE_PARKING_CNT}${translateBike(PageLocale)}</div>`)
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
                .bindPopup(`<strong>${m.SBIKE_SPOT_NM}</strong><br><br><div class="bike-count-bubble">${m.SBIKE_PARKING_CNT}${translateBike(PageLocale)}</div>`)
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

document.addEventListener('DOMContentLoaded', async () => {
    //지도 렌더링
    
    try{
        const url = new URL(window.location.href);
        const attractionId = url.pathname.split('/')[3];
        const apiResponse = await fetch(`/${PageLocale}/bike/${attractionId}`);
        const resBody = await apiResponse.json();
        const bikeData = await resBody.SBIKE_STTS;

        const initLat = bikeData[0].SBIKE_X;
        const initLng = bikeData[0].SBIKE_Y;
        
        const bikeList = document.querySelector('.bike-list');

        for (bike of bikeData) {
            const bikeItem = document.createElement('li');

            const bikeStationName = document.createElement('span');
            bikeStationName.textContent = bike.SBIKE_SPOT_NM
            bikeStationName.classList.add('bike-station-name');
            
            const bikeCount = document.createElement('span');
            bikeCount.textContent = bike.SBIKE_PARKING_CNT;
            
            bikeCount.classList.add('bike-count-list');
            if (bike.SBIKE_PARKING_CNT == '0') {
                bikeCount.classList.add('bike-zero');
            }
            bikeItem.appendChild(bikeCount);
            bikeItem.appendChild(bikeStationName);
            bikeList.appendChild(bikeItem);
        };

        let map = L.map('map', {
            center: [initLat, initLng],
            zoom: 16,
        });
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
        circleOnMap(bikeData, map)

        const totalBikesHeader = document.getElementById('total-bikes');
        if (totalBikesHeader && Array.isArray(bikeData) && bikeData.length > 0) {
            const total = bikeData.reduce((s, st) => s + (parseInt(st.SBIKE_PARKING_CNT, 10) || 0), 0);
            const result = totalBikesHeader.innerText.replace('--counts--', total);
            totalBikesHeader.textContent = result;
        } else {
            const result = totalBikesHeader.innerText.replace('--counts--', 0);
            totalBikesHeader.textContent = result;
        }

    } catch {
        const msgNoBike = document.createElement('div')
        msgNoBike.textContent = 'No bike available'
        msgNoBike.classList.add('no-bike')
        document.getElementById('map').appendChild(msgNoBike)
    }
})