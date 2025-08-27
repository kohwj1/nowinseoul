from flask import Flask, render_template, jsonify, url_for, request
from services.bike_station_fetcher import get_info
from models import db
import os

#테스트 데이터 불러오기 위한 모듈입니다. 배포 전 삭제 필요!
import json
from testgen.test_map_data_generator import mapdata_generator

app = Flask(__name__, instance_relative_config=True) # instance 폴더가 앱 설정과 리소스 파일들의 기준 경로로 사용됩
app.config['DATABASE'] = os.path.join(app.instance_path, 'nowinseoul.db')

# 메인 페이지
@app.route('/', methods=['GET','POST'])
def index():
    data = db.get_images([])

    return render_template('index.html', data = data)

# 지도 페이지
@app.route('/map')
def browse_on_map():
    mapdata = mapdata_generator()
    return render_template('onmap.html', data={"data":mapdata})

# 상세 페이지
@app.route('/detail/<attraction_id>')
def detail(attraction_id):
    attraction_info_by_id = db.get_info_by_id('attraction', attraction_id)
    if not attraction_info_by_id:
        return render_template('404.html'), 404

    data = {"AREA_CD" : attraction_id,
            "NAME" : attraction_info_by_id[0].get('name_en'),
            "DESCRIPTION": attraction_info_by_id[0].get('description'),
            "WEATHER_STTS": [{"FCST_DT": d.get('fcst_dt'),
                              "TEMP": str(d.get('fcst_temp')),
                              "RAIN_CHANCE": str(d.get('rain_chance'))}
                              for d in db.get_info_by_id('weather_cache',attraction_id)
            ], # 12개
            "AREA_PPLTN":[{"FCST_TIME": d.get('realtime_pop_dttm'),
                           "FCST_CONGEST_LVL": d.get('realtime_pop')}
                              for d in db.get_info_by_id('detail_cache',attraction_id)
            ],
            "ROAD_TRAFFIC_STTS":[{"ROAD_TRAFFIC_TIME": d.get('realtime_road_dttm'),
                                  "ROAD_TRAFFIC_IDX": d.get('realtime_road')}
                              for d in db.get_info_by_id('detail_cache',attraction_id)
            ],
            "SBIKE_STTS":get_info(attraction_id)
    }
    print(data)
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