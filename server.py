from flask import Flask, request, render_template
from flask import render_template, request, jsonify
import requests


app = Flask(__name__)
_rotInfo, _xyz = {}, [0, 0, 0]


@app.route('/')
def index():
    return jsonify("🌵 . . |=~this-is-empty~=| .. . 🌵")


@app.route('/coords/pos/set', methods=['POST', 'GET'])
def set_pos():
    global _rotInfo, _xyz
    if request.method == 'POST':
        data = request.json
        _xyz = data['xyz']
        # _rotInfo = data['rotInfo']
        url = 'http://127.0.0.1:5001//coords/info/get'
        data = {'xyz': _xyz, "rotInfo": _rotInfo}
        return_data = requests.post(url, json=data)
        if return_data.ok:
            return return_data.json()
    return jsonify("error")


@app.route('/coords/info/get', methods=['GET'])
def get_info():
    global _rotInfo, _xyz
    return jsonify({'rotInfo': _rotInfo, 'xyz': _xyz})


@app.route('/coords/rot/set', methods=['POST'])
def set_rot():
    global _rotInfo, _xyz
    if request.method == 'POST':
        data = request.json
        # _xyz = data['xyz']
        _rotInfo = data['rotInfo']
    return jsonify("ok")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
