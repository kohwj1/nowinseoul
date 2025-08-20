document.addEventListener('DOMContentLoaded', () => {
    // 1. readMoreBtn 기능
    const textContainer = document.querySelector('.text-container');
    const readMoreBtn = document.getElementById('read-more-btn');

    readMoreBtn.addEventListener('click', () => {
        textContainer.classList.toggle('expanded');
        if (textContainer.classList.contains('expanded')) {
            readMoreBtn.textContent = 'Read less';
        } else {
            readMoreBtn.textContent = 'Read more';
        }
    });

    // 2. 군중 밀도 그래프 (crowd-density-bar)
    const crowdDataElement = document.getElementById('crowd-data-json');

    if (crowdDataElement) {
        try {
            const crowdData = JSON.parse(crowdDataElement.textContent);
            const progressBar = document.getElementById('crowd-density-bar');

            crowdData.forEach((value, index) => {
                const segment = document.createElement('span');
                segment.classList.add('progress-bar-segment');

                let color;
                if (value >= 0.8) {
                    color = 'red';
                } else if (value >= 0.6) {
                    color = 'orange';
                } else if (value >= 0.4) {
                    color = 'yellow';
                } else {
                    color = 'green';
                }

                segment.style.backgroundColor = color;
                segment.style.width = `24%`;
                progressBar.appendChild(segment);
            });

        } catch (error) {
            console.error('군중 밀도 데이터 파싱 오류:', error);
        }
    }

    // 3. 공공 자전거 정보 (public-bike-section)
    const bikeDataElement = document.getElementById('bike-data-json');

    if (bikeDataElement) {
        try {
            const bikeStations = JSON.parse(bikeDataElement.textContent);
            const totalBikes = bikeStations.reduce((sum, station) => {
                return sum + parseInt(station.SBIKE_PARKING_CNT, 10);
            }, 0);

            const bikeHeader = document.querySelector('total-bikes');

            if (bikeHeader) {
                bikeHeader.textContent = `${totalBikes} Public bike(s) available`;
            }

        } catch (error) {
            console.error('자전거 데이터 파싱 오류:', error);
        }
    }
});