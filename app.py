from flask import Flask, render_template, jsonify, url_for, request
from services.bike_station_fetcher import get_info
from models import db
import os


app = Flask(__name__)

# 메인 페이지
@app.route('/')
def index():
    data = db.get_images([])

    return render_template('index.html', data = data)

# 지도 페이지
@app.route('/map')
def browse_on_map():
    # [{'id': 'POI001', 'name': 'Gangnam MICE Special Tourist Zone', 'crowd': 'Crowded', 'beauty': '241', 'food': '25', 'drama': '18', 'movie': '14', 'lat': '37.512693', 'lng': '127.0624'},]
    data = db.get_info_for_map()
        
    return render_template('onmap.html', data=data)

# 상세 페이지
@app.route('/detail/<attraction_id>')
def detail(attraction_id):
    attraction_info_by_id = db.get_info_by_id('attraction', attraction_id)
    if not attraction_info_by_id:

        return render_template('404.html'), 404

    data = {"AREA_CD" : attraction_id,
            "NAME" : attraction_info_by_id[0].get('name_en'),
            "DESC_KO": attraction_info_by_id[0].get('desc_ko'),
            "DESC_EN": attraction_info_by_id[0].get('desc_en'),
            "DESC_JA": attraction_info_by_id[0].get('desc_ja'),
            # 날씨 예측
            "WEATHER_STTS": [{"FCST_DT": d.get('fcst_dt'),
                              "TEMP": str(d.get('fcst_temp')),
                              "RAIN_CHANCE": str(d.get('rain_chance'))}
                              for d in db.get_info_by_id('weather_cache',attraction_id)
            ], # 12개
            # 인구밀도 예측
            "FCST_PPLTN":[{"FCST_TIME": d.get('fcst_dt'),
                           "FCST_CONGEST_LVL": d.get('level')}
                              for d in db.get_info_by_id('density_cache',attraction_id)
            ],
            # 실시간 인구밀도
            "LIVE_PPLTN_STTS":[{"PPLTN_TIME": d.get('realtime_pop_dttm'),
                                "AREA_CONGEST_LVL": d.get('realtime_pop')}
                                   for d in db.get_info_by_id('detail_cache',attraction_id)
            ],
            # 실시간 주변도로 혼잡도
            "ROAD_TRAFFIC_STTS":[{"ROAD_TRAFFIC_TIME": d.get('realtime_road_dttm'),
                                  "ROAD_TRAFFIC_IDX": d.get('realtime_road')}
                              for d in db.get_info_by_id('detail_cache',attraction_id)
            ],
            # 주변 따릉이
            # {'SBIKE_SPOT_NM_KO': '379. 서울역9번출구', 'SBIKE_SPOT_NM_EN': '379. Seoul Station Exit 9', 'SBIKE_SPOT_NM_JA': '379.ソウル駅9番出口', 'SBIKE_PARKING_CNT': '5', 'SBIKE_X': '37.55599976', 'SBIKE_Y': '126.97335815'}
            "SBIKE_STTS":get_info(attraction_id)
    }

    return render_template('detail_page.html', data=data)

# --------------------------------------------

# 메인에서 태그 필터 걸때
@app.route('/main-feature', methods=['POST'])
def filter_by_tags():
    tags = request.form.get('tags')
    data = {"tags" : tags,
            "data" : db.get_images(tags)
    }

    return jsonify(data)

# --------------------------------------------

# https://flask.palletsprojects.com/en/stable/errorhandling/
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly

    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)