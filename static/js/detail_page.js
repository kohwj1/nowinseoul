document.addEventListener('DOMContentLoaded', () => {
    // 1. readMoreBtn functionality
    const textContainer = document.querySelector('.text-container');
    const readMoreBtn = document.getElementById('read-more-btn');

    if (textContainer && readMoreBtn) {
        readMoreBtn.addEventListener('click', () => {
            textContainer.classList.toggle('expanded');
            if (textContainer.classList.contains('expanded')) {
                readMoreBtn.textContent = 'Read less';
            } else {
                readMoreBtn.textContent = 'Read more';
            }
    });
    }

    // 2. Crowd density graph (crowd-density-bar)
    const crowdDataElement = document.getElementById('crowd-data-json');
    const progressBar = document.getElementById('crowd-density-bar');

    // Get the crowd tag and time labels
    const crowdTag = document.getElementById('traffic-tag');
    const timeNow = document.getElementById('time-now');
    const time1 = document.getElementById('time-1');
    const time2 = document.getElementById('time-2');
    const time3 = document.getElementById('time-3');

    if (crowdDataElement && progressBar) {
        try {
            const crowdData = JSON.parse(crowdDataElement.textContent);
            const now = new Date();
            const currentHour = now.getHours();

            // Find the current congestion level and update the tag
            const currentCongestionData = crowdData.find(item => {
                const itemHour = new Date(item.FCST_TIME).getHours();
                return itemHour === currentHour;
            });

            if (currentCongestionData) {
                crowdTag.textContent = currentCongestionData.FCST_CONGEST_LVL;
            }

            // Slice the data to show the next 4 hours
            const upcomingData = crowdData.filter(item => {
                const itemDate = new Date(item.FCST_TIME);
                return itemDate.getHours() >= currentHour && itemDate.getDate() === now.getDate();
            }).slice(0, 4);

            // Clear existing segments before adding new ones
            progressBar.innerHTML = '';

            upcomingData.forEach((item, index) => {
                const segment = document.createElement('span');
                segment.classList.add('progress-bar-segment');

                let color;
                switch (item.FCST_CONGEST_LVL) {
                    case 'Comfortable':
                        color = 'green';
                        break;
                    case 'Moderate':
                        color = 'yellow';
                        break;
                    case 'Crowded':
                        color = 'orange';
                        break;
                    case 'Very Crowded':
                        color = 'red';
                        break;
                    default:
                        color = 'gray'; // Default for unknown status
                }

                segment.style.backgroundColor = color;
                progressBar.appendChild(segment);

                // Update the time labels
                const itemTime = new Date(item.FCST_TIME);
                const itemHour = itemTime.getHours();
                if (index === 0) {
                    // "Now" is a fixed label
                } else if (index === 1) {
                    time1.textContent = `${itemHour}h`;
                } else if (index === 2) {
                    time2.textContent = `${itemHour}h`;
                } else if (index === 3) {
                    time3.textContent = `${itemHour}h`;
                }
            });

        } catch (error) {
            console.error('Crowd density data parsing error:', error);
        }
    }

    // 3. Public bike information (public-bike-section)
    const bikeDataElement = document.getElementById('bike-data-json');
    const totalBikesHeader = document.getElementById('total-bikes');

    if (bikeDataElement && totalBikesHeader) {
        try {
            const bikeStations = JSON.parse(bikeDataElement.textContent);
            const totalBikes = bikeStations.reduce((sum, station) => {
                return sum + parseInt(station.SBIKE_PARKING_CNT, 10);
            }, 0);

            totalBikesHeader.textContent = `${totalBikes} Public bike(s) available`;
        } catch (error) {
            console.error('Bike data parsing error:', error);
        }
    }
    
    // 4. Weather Forecast
    const weatherDataElement = document.getElementById('weather-data-json');
    const weatherForecastContainer = document.querySelector('.weather-forecast');
    
    if (weatherDataElement && weatherForecastContainer) {
        try {
            const weatherData = JSON.parse(weatherDataElement.textContent);
            
            // Clear existing items
            weatherForecastContainer.innerHTML = '';
            
            // Filter and get the next 4 hours
            const now = new Date();
            const currentHour = now.getHours();
            
            const upcomingWeather = weatherData.filter(item => {
                const itemHour = parseInt(item.FCST_DT.slice(8, 10));
                return itemHour >= currentHour;
            }).slice(0, 4);

            upcomingWeather.forEach(item => {
                const forecastItem = document.createElement('div');
                forecastItem.classList.add('forecast-item');
                
                const time = document.createElement('span');
                time.classList.add('time');
                time.textContent = `${parseInt(item.FCST_DT.slice(8, 10))}h`;
                
                const temp = document.createElement('span');
                temp.classList.add('temp');
                temp.textContent = `${item.TEMP}°C`;
                
                const rainChanceGraph = document.createElement('div');
                rainChanceGraph.classList.add('rain-chance-graph');
                
                const rainChance = document.createElement('div');
                rainChance.classList.add('rain-chance');
                rainChance.textContent = `${item.RAIN_CHANCE}%`;
                
                forecastItem.appendChild(time);
                forecastItem.appendChild(temp);
                forecastItem.appendChild(rainChanceGraph);
                forecastItem.appendChild(rainChance);
                
                weatherForecastContainer.appendChild(forecastItem);
            });
            
            // Update current temperature
            const currentTempSpan = document.querySelector('.current-temp');
            if (currentTempSpan && upcomingWeather.length > 0) {
                currentTempSpan.textContent = `${upcomingWeather[0].TEMP}°C`;
            }
        } catch (error) {
            console.error('Weather data parsing error:', error);
        }
    }
});