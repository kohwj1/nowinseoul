from flask import Flask, render_template, jsonify

app = Flask(__name__)

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
    return render_template('index.html')

# --------------------------------------------

# 메인 페이지에서 태그 선택시
@app.route('/main-feature', methods=['POST'])
def index():
    return jsonify({"tags":['food','movie'],
                    "data":[
                        {"id" : "POI095", "name" : "Banpo Hangang Park"},
                        {"id" : "POI096", "name" : "Dream Forest"},
                        {"id" : "POI098", "name" : "Seoripul Park·Montmartre Park"},
                        {"id" : "POI099", "name" : "Seoul Plaza"},
                        {"id" : "POI100", "name" : "Seoul Grand Park"},
                        {"id" : "POI101", "name" : "Seoul Forest"},
                    ]
    })

# 지도 페이지에서 조건/검색 선택시
@app.route('/map-pin', methods=['POST'])
def index():
    return jsonify({"message":"not yet"})

if __name__ == '__main__':
    app.run(debug=True)