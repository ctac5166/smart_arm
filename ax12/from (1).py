from flask import Flask, render_template, jsonify
from ax12.test import coordinate_interpreter

# initializing a variable of Flask
app = Flask(__name__)


# decorating index function with the app.route with url as /login
@app.route('/')
@app.route('/map')
def index():
    return render_template('map.html')


@app.route('/FlaskTutorial', methods=['GET', 'POST'])
def success():
    from flask import request
    data = request.json
    coordinate_interpreter(data)
    print(data)
    return jsonify({"end":"ok"})

if __name__ == "__main__":
    app.run(debug=True)
