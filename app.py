from flask import Flask, render_template, jsonify
import os

app = Flask(__name__, instance_relative_config=True) # instance 폴더가 앱 설정과 리소스 파일들의 기준 경로로 사용됩
app.config['DATABASE'] = os.path.join(app.instance_path, 'nowinseoul.db')

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 지도 페이지
@app.route('/map')
def browse_on_map():
    return render_template('index.html')

# 상세 페이지
@app.route('/detail/<id>')
def detail():
    return render_template('detail_page.html')

# --------------------------------------------

# 메인에서 태그 필터 걸때
@app.route('/main-feature', methods=['POST'])
def index():
    return render_template('index.html', data = {"tags" : ["food", "movie"],
        "data":[
            {'id':'POI095','thumnail':'POI095.jpg','name': 'Banpo Hangang Park'},
            {'id':'POI096','thumnail':'POI096.png','name': 'Dream Forest'},
            {'id':'POI098','thumnail':'POI098.jpg','name': 'Seoripul Park·Montmartre Park'},
            {'id':'POI099','thumnail':'POI099.jpg','name': 'Seoul Plaza'},
            {'id':'POI100','thumnail':'POI100.png','name': 'Seoul Grand Park'},
            {'id':'POI101','thumnail':'POI101.png','name': 'Seoul Forest'},
        ]
    })

# 지도에서 조건 걸때
@app.route('/map-pin', methods=['POST'])
def index():
    return jsonify({"message":"not yet"})

if __name__ == '__main__':
    app.run(debug=True)