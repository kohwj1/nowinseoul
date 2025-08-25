from flask import Flask, render_template, jsonify, url_for
from services.bike_station_fetcher import get_info
import os

#테스트 데이터 불러오기 위한 모듈입니다. 배포 전 삭제 필요!
import json
from testgen.test_map_data_generator import mapdata_generator

app = Flask(__name__, instance_relative_config=True) # instance 폴더가 앱 설정과 리소스 파일들의 기준 경로로 사용됩
app.config['DATABASE'] = os.path.join(app.instance_path, 'nowinseoul.db')

# 메인 페이지
@app.route('/', methods=['GET','POST'])
def index():
    data = [
            {'id':'POI095','name': 'Banpo Hangang Park'},
            {'id':'POI096','name': 'Dream Forest'},
            {'id':'POI098','name': 'Seoripul Park·Montmartre Park'},
            {'id':'POI099','name': 'Seoul Plaza'},
            {'id':'POI100','name': 'Seoul Grand Park'},
            {'id':'POI101','name': 'Seoul Forest'},
           
    ]

    if request.method == "POST":
        # POST 에 대한 처리
        tags = request.form["tags"] #list
        return 


    return render_template('index.html', data = data)

# 지도 페이지
@app.route('/map')
def browse_on_map():
    mapdata = mapdata_generator()
    return render_template('onmap.html', data={"data":mapdata})

# 상세 페이지
@app.route('/detail/<id>/<name>')
def detail(id, name):
    data = {"AREA_CD":id,
            "NAME":name,
            # "LAST_UPDATE_DTTM": db.get_id_info(id).get('insert_dttm')
            # DB에 아직 없음 "DESCRIPTION":db.get_id_info(id).get('description'),
            "DESCRIPTION": "Seoul Station, nestled in the heart of South Korea's vibrant capital, is far more than just a transit hub—it's a cultural landmark that beautifully marries the past with the present. As a pivotal gateway to Seoul, this bustling station offers travelers an intriguing blend of modernity and tradition. Whether you're arriving from Incheon Airport or embarking on a high-speed KTX train to explore the rest of Korea, Seoul Station ensures a seamless travel experience with its extensive connections and top-notch amenities. Beyond its role as a transportation center, it invites visitors to delve into the rich history and vibrant culture of Seoul, making it an essential stop for history buffs, culture enthusiasts, and travelers alike.",
            "WEATHER_STTS": [j # 12개
                {
                    "FCST_DT": "202508210400",
                    "TEMP": "27",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508210500",
                    "TEMP": "27",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508210600",
                    "TEMP": "26",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508210700",
                    "TEMP": "26",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508210800",
                    "TEMP": "26",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508210900",
                    "TEMP": "27",
                    "RAIN_CHANCE": "60",
                },
                {
                    "FCST_DT": "202508211000",
                    "PRECPT_TYPE": "소나기",
                    "RAIN_CHANCE": "60",
                },
                {
                    "FCST_DT": "202508211100",
                    "TEMP": "30",
                    "RAIN_CHANCE": "60",
                },
                {
                    "FCST_DT": "202508211200",
                    "TEMP": "30",
                    "RAIN_CHANCE": "30",
                },
                {
                    "FCST_DT": "202508211300",
                    "TEMP": "31",
                    "RAIN_CHANCE": "30",
                },
                {
                    "FCST_DT": "202508211400",
                    "TEMP": "31",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508211500",
                    "TEMP": "31",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508211600",
                    "TEMP": "31",
                    "RAIN_CHANCE": "0",
                },
                {
                    "FCST_DT": "202508211700",
                    "TEMP": "31",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508211800",
                    "TEMP": "31",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508211900",
                    "TEMP": "29",
                    "RAIN_CHANCE": "0",
                },
                {
                    "FCST_DT": "202508212000",
                    "TEMP": "29",
                    "RAIN_CHANCE": "0",
                },
                {
                    "FCST_DT": "202508212100",
                    "TEMP": "28",
                    "RAIN_CHANCE": "0",
                },
                {
                    "FCST_DT": "202508212200",
                    "TEMP": "28",
                    "RAIN_CHANCE": "0",
                },
                {
                    "FCST_DT": "202508212300",
                    "TEMP": "27",
                    "RAIN_CHANCE": "20",
                },
                {
                    "FCST_DT": "202508220000",
                    "TEMP": "27",
                    "RAIN_CHANCE": "0",
                },
                {
                    "FCST_DT": "202508220100",
                    "TEMP": "27",
                    "RAIN_CHANCE": "30",
                },
                {
                    "FCST_DT": "202508220200",
                    "TEMP": "26",
                    "RAIN_CHANCE": "30",
                },
                {
                    "FCST_DT": "202508220300",
                    "TEMP": "26",
                    "RAIN_CHANCE": "30",
                }
            ],
            "AREA_PPLTN":[
                {
                    "FCST_TIME": "2025-08-21 04:00",
                    "FCST_CONGEST_LVL": "Comfortable",
                },
                {
                    "FCST_TIME": "2025-08-21 05:00",
                    "FCST_CONGEST_LVL": "Comfortable",
                },
                {
                    "FCST_TIME": "2025-08-21 06:00",
                    "FCST_CONGEST_LVL": "Comfortable",
                },
                {
                    "FCST_TIME": "2025-08-21 07:00",
                    "FCST_CONGEST_LVL": "Comfortable",
                },
                {
                    "FCST_TIME": "2025-08-21 08:00",
                    "FCST_CONGEST_LVL": "Comfortable",
                },
                {
                    "FCST_TIME": "2025-08-21 09:00",
                    "FCST_CONGEST_LVL": "Moderate",
                },
                {
                    "FCST_TIME": "2025-08-21 10:00",
                    "FCST_CONGEST_LVL": "Crowded",
                },
                {
                    "FCST_TIME": "2025-08-21 11:00",
                    "FCST_CONGEST_LVL": "Crowded",
                },
                {
                    "FCST_TIME": "2025-08-21 12:00",
                    "FCST_CONGEST_LVL": "Crowded",
                },
                {
                    "FCST_TIME": "2025-08-21 13:00",
                    "FCST_CONGEST_LVL": "Crowded",
                },
                {
                    "FCST_TIME": "2025-08-21 14:00",
                    "FCST_CONGEST_LVL": "Crowded",
                },
                {
                    "FCST_TIME": "2025-08-21 15:00",
                    "FCST_CONGEST_LVL": "Crowded",
                }
            ],
            "SBIKE_STTS":get_info(id)
    }
    print(data)
    return render_template('detail_page.html', data=data)

# --------------------------------------------

# 메인에서 태그 필터 걸때
@app.route('/main-feature', methods=['POST'])
def filter_by_tags():
    data = {"tags" : ["food", "movie"],
        "data":[
            {'id':'POI095','name': 'Banpo Hangang Park'},
            {'id':'POI096','name': 'Dream Forest'},
            {'id':'POI098','name': 'Seoripul Park·Montmartre Park'},
            {'id':'POI099','name': 'Seoul Plaza'},
            {'id':'POI100','name': 'Seoul Grand Park'},
            {'id':'POI101','name': 'Seoul Forest'},
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)