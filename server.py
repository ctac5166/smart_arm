import time
from flask import Flask, Response, request, render_template
from flask import render_template, request, jsonify
import requests
import sqlite3
import cv2
import threading


conn = sqlite3.connect('db/database.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users_info(
   user_ip TEXT,
   position_x TEXT,
   position_y TEXT,
   position_z TEXT,
   rotation_table TEXT,
   rotation_a TEXT,
   rotation_b TEXT,
   rotation_c TEXT)
""")
conn.commit()

app = Flask(__name__)
_rotInfo, _xyz = {}, [0, 0, 0]


def db_get_info(component_to_selected, selected_group, name_of_column, where_comp_value):
    global cur

    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()

    sqlite_select_query = f"SELECT {component_to_selected} from {selected_group} WHERE {name_of_column} = ?"
    cur.execute(sqlite_select_query, (where_comp_value,))
    exit_data = cur.fetchall()
    return exit_data


def db_set_new_info(component_to_selected, selected_group, name_of_column, where_comp_value, new_data):
    global cur

    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()

    if db_get_info(component_to_selected, selected_group, name_of_column, where_comp_value):
        sql = f"UPDATE users_info SET rotation_table = ?, rotation_a = ?, rotation_b = ?, rotation_c = ? WHERE user_ip = ?"
        val = (new_data, where_comp_value)
        cur.execute(sql, val)
        conn.commit()
        return None

    val = [name_of_column, "", "", "", "", "", "", ""]
    sql = f"""INSERT INTO users_info VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""
    cur.executemany(sql, val)
    conn.commit()
    db_set_new_info(component_to_selected, selected_group, name_of_column, where_comp_value, new_data)


@app.route('/', methods=["GET"])
def index():
    return "hello!"


@app.route('/get_speed', methods=['POST', 'GET'])
def get_speed():
    url = 'http://169.254.69.215:5000/get_speed'
    return_data = requests.post(url)
    print(return_data)
    if return_data.ok:
        return_data = return_data.json()
        return_data = return_data['speed']
        k = 0
        for i in return_data:
            return_data[k] = str(i)
            k += 1
        return f"{return_data[0]};{return_data[1]};{return_data[2]};{return_data[3]};{return_data[4]}"


@app.route('/get_temp', methods=['POST', 'GET'])
def get_temp():
    url = 'http://169.254.69.215:5000/get_temperature'
    return_data = requests.post(url)
    print(return_data)
    if return_data.ok:
        return_data = return_data.json()
        return_data = return_data['temperature']
        k = 0
        for i in return_data:
            return_data[k] = str(i)
            k += 1
        return f"{return_data[0]};{return_data[1]};{return_data[2]};{return_data[3]};{return_data[4]}"


@app.route('/pos/set/vr', methods=['POST', 'GET'])
def sewt_vr_pos():
    # print(request.args.get('val'))
    global _rotInfo, _xyz
    print(request.json)

    data = request.json
    print(data)
    _xyz = data['xyz']
    speed = data['speed']
    # _rotInfo = data['rotInfo']
    url = 'http://192.168.0.23:8080/coords/info/get'
    data = {'xyz': _xyz, 'speed': data['speed'], 'rot': data['rotation'], 'opened': data['opened'], "rot2": data['rotation2']}
    return_data = requests.post(url, json=data)
    print(return_data)
    if return_data.ok:
        return_data = return_data.json()
        _rotInfo = return_data['rotInfo']
        print(return_data)
        return f"{return_data['return']};{_rotInfo[0]};{_rotInfo[1]};{_rotInfo[2]};{_rotInfo[3]}"
    return '404'

@app.route('/pos/set', methods=['POST', 'GET'])
def set_pos():
    global _rotInfo, _xyz
    if request.method == 'POST':
        data = request.json
        print(data)
        _xyz = data['xyz']
        # _rotInfo = data['rotInfo']
        url = 'http://192.168.0.23:8080/coords/info/get'
        data = {'xyz': _xyz, 'speed': data['speed'], "rot": data['rotation']}
        return_data = requests.post(url, json=data)
        print(return_data)
        if return_data.ok:
            return_data = return_data.json()
            _rotInfo = return_data['rotInfo']
            # db_set_new_info('rotation_table = ?, rotation_a = ?, rotation_b = ?, rotation_c',
            #                 'users_info', 'user_ip', str(request.remote_addr), return_data)

            # return_data = return_data.json()
            # return return_data['']
            return jsonify({"returned": return_data['return'], "rotInfo": _rotInfo})
        else:
            return "server-error"
        return "server-error"

    return "server-error"


@app.route('/rot/get', methods=['GET'])
def rot_set():
    global _rotInfo, _xyz
    # user_data = db_get_info('*', 'users_info', 'user_ip', str(request.remote_addr))
    # if user_data:
    try:
        return str(_rotInfo[0] + ";" + _rotInfo[1] + ";" + _rotInfo[2] + ";" + _rotInfo[3])
    except Exception:
        return "0;0;0;0"


@app.route('/pos/get', methods=['GET'])
def pos_set():
    global _rotInfo, _xyz
    # user_data = db_get_info('*', 'users_info', 'user_ip', str(request.remote_addr))
    # if user_data:э
    print( str(_xyz[0] + ";" + _xyz[1] + ";" + _xyz[2]))
    return str(_xyz[0] + ";" + _xyz[1] + ";" + _xyz[2])
    return "0;0;0;"


@app.route('/coords/all/set', methods=['POST'])
def set_native_info():
    global _rotInfo, _xyz
    if request.method == 'POST':
        data = request.json
        # _xyz = data['xyz']
        _rotInfo = data['rotInfo']

        k = 0
        for i in _rotInfo:
            _rotInfo[k] = str(i)
            k += 1

        db_set_new_info('rotation_table = ?, rotation_a = ?, rotation_b = ?, rotation_c',
                        'users_info', 'user_ip', str(request.remote_addr), _rotInfo)

    return jsonify("ok")


if __name__ == "__main__":
    app.run(host="192.168.0.109",debug=True, port=5000)
