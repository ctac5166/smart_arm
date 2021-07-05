from flask import Flask, request, render_template
from flask import render_template, request, jsonify
import requests


app = Flask(__name__)
_rotInfo, _xyz = {}, [0, 0, 0]


@app.route('/')
def index():
    return jsonify("🌵 . . |=~this-is-empty~=| .. . 🌵")


@app.route('/coords/pos/set', methods=['POST'])
def set_pos():
    global _rotInfo, _xyz
    if request.method == 'POST':
        data = request.json
        _xyz = data['xyz']
        # _rotInfo = data['rotInfo']
    return jsonify("ok")


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
    app.run(debug=True)
