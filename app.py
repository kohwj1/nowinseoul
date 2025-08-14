from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map-pin')
def browse_on_map():
    return render_template('index.html')

@app.route('/detail/<id>')
def detail():
    return render_template('index.html')

# --------------------------------------------

@app.route('/main-feature', methods=['POST'])
def index():
    return jsonify("message":"not yet")

if __name__ == '__main__':
    app.run(debug=True)