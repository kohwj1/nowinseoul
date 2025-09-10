from flask import Flask, render_template, jsonify, request, current_app, redirect, url_for, Blueprint
from flask_babel import Babel
from services.bike_station_fetcher import get_info
from models import db
import utils


app = Flask(__name__) # 앱 인스턴스 : 앱 전체의 생명주기 동안 존재하는 단일 객체

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ko', 'en', 'ja']

# 다국어 지원
babel = Babel(app)

def get_locale():
    # https://flask.palletsprojects.com/en/stable/api/#flask.Request.view_args
    # Flask 웹 프레임워크에서 URL 경로(path) 요소로부터 추출된 변수(locale)를 의미
    path_lang = request.view_args.get('locale', False)
    if path_lang in current_app.config['BABEL_SUPPORTED_LOCALES']:
        return path_lang

    # https://python-babel.github.io/flask-babel/
    # try to guess the language from the user accept header the browser transmits.
    # We support ko/en/ja in this app. The best match wins.
    return request.accept_languages.best_match(current_app.config['BABEL_SUPPORTED_LOCALES'])
    # 이걸 이용해서 ko, en, ja로 케이스 분기처리되면 됩니다!

babel.init_app(app, locale_selector=get_locale) # 언어는 url의 locale을 따른다

# https://flask.palletsprojects.com/en/stable/appcontext/
# 앱 시작할 때, 언어별 tag조합별 id/name 목록을 생성해서 current_app에 캐싱
@app.before_request
def initialize_cache():
    current_app.config['tag_cases'] = db.generate_tag_cases()

@app.route('/')
def root():
    # url/에 처음 들어오면 clinet browser의 언어설정을 가져오는데, false면 default 값 적용
    locale = request.accept_languages.best_match(current_app.config['BABEL_SUPPORTED_LOCALES']) or current_app.config['BABEL_DEFAULT_LOCALE']

    return redirect(url_for('main.index', locale=locale))

main = Blueprint('main', __name__, url_prefix='/<locale>')

# 메인 페이지
@main.route('/')
def index(locale):
    print(f'\n{get_client_ip()} 에서 방문했습니다.')
    data = current_app.config.get('tag_cases', {}).get(locale, {})# browser url <locale> 값이 기본값

    return render_template('index.html', data = data, locale=locale)

def get_client_ip():
    # X-Forwarded-For 헤더: 클라이언트가 프록시 서버를 거칠 때 원래 IP 정보가 담긴 헤더
    # X-Real-IP 헤더: 일부 프록시(예: Nginx)에서 설정하는 클라이언트 IP
    # 둘 다 없으면 request.remote_addr가 fallback(일반적으로 직접 연결 IP) 없으면 remote_addr 사용
    ip = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
    return f"Client IP: {ip}"

# 지도 페이지
@main.route('/map')
def browse_on_map(locale):
    # route 변수 검증
    if locale not in current_app.config['BABEL_SUPPORTED_LOCALES']:
        return render_template('404.html'), 404
        
    data = db.get_info_for_map(locale) # browser locale 값이 기본값
        
    return render_template('onmap.html', data = data, locale=locale)

# 상세 페이지
@main.route('/detail/<attraction_id>')
def detail(locale, attraction_id):
    attraction_info_by_id = db.get_info_by_id('attraction', attraction_id)
    # route 변수 검증
    if locale not in current_app.config['BABEL_SUPPORTED_LOCALES'] or not attraction_info_by_id:
        return render_template('404.html'), 404

    detail_cache_data = db.get_info_by_id('detail_cache',attraction_id)
    data = {"AREA_CD" : attraction_id,
            "NAME" : attraction_info_by_id[0].get('name_' + locale),
            "DESCRIPTION": attraction_info_by_id[0].get('desc_' + locale),
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
                                    for d in detail_cache_data
            ],
            # 실시간 주변도로 혼잡도
            "ROAD_TRAFFIC_STTS":[{"ROAD_TRAFFIC_TIME" : d.get('realtime_road_dttm'),
                                  "ROAD_TRAFFIC_IDX" : d.get('realtime_road'),
                                  "ROAD_MSG" : d.get('realtime_road_msg')}
                                    for d in detail_cache_data
            ]
    }

    return render_template('detail_page.html', data=data, locale=locale)

# --------------------------------------------

# 따릉이
@main.route('/bike/<attraction_id>')
def bike(locale, attraction_id):
    # route 변수 검증
    if locale not in current_app.config['BABEL_SUPPORTED_LOCALES'] or attraction_id not in db.Attractions().get_id():
        return render_template('404.html'), 404

    # 주변 따릉이
    # {'SBIKE_SPOT_NM_KO': '379. 서울역9번출구', 'SBIKE_SPOT_NM_EN': '379. Seoul Station Exit 9', 'SBIKE_SPOT_NM_JA': '379.ソウル駅9番出口', 'SBIKE_PARKING_CNT': '5', 'SBIKE_X': '37.55599976', 'SBIKE_Y': '126.97335815'}
    return jsonify({"SBIKE_STTS":get_info(attraction_id, locale)})

# --------------------------------------------

# https://flask.palletsprojects.com/en/stable/errorhandling/
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly

    return render_template('404.html'), 404

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(host='0.0.0.0')