from flask import Flask, Response, request, render_template
from flask import render_template, request, jsonify
import requests
import sqlite3
from flask_login import LoginManager


import socket


conn = sqlite3.connect(r'db/orders.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users_data(
   userid TEXT PRIMARY KEY,
   x REAL,
   y REAL,
   z REAL,
   grip_open REAL,
   grip_rot REAL,
   last_link_rot REAL,
   speed REAL
   );
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS manip_data(
   userid TEXT PRIMARY KEY,
   table_rot REAL,
   alf1 REAL,
   alf2 REAL,
   alf3 REAL,
   alf4 REAL,
   status TEXT,
   speed REAL);
""")
conn.commit()


def insert_data(user, table_name, values_cont):
    try:

        with sqlite3.connect(r'db/orders.db') as conn:
            cur = conn.cursor()
            cur.execute(f"""INSERT INTO {table_name} VALUES{values_cont};""", user)
            conn.commit()

        # conn = sqlite3.connect(r'db/orders.db', timeout=10)
        # cur = conn.cursor()
        # cur.execute(f"""INSERT INTO {table_name} VALUES{values_cont};""", user)
        # conn.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def select_all_from(user_id, table_name):
    try:
        with sqlite3.connect(r'db/orders.db') as conn:
            cur = conn.cursor()
            sql_select_query = f"""select * from {table_name} where userid = ?"""
            cur.execute(sql_select_query, (user_id,))
            conn.commit()
        # conn = sqlite3.connect(r'db/orders.db', timeout=10)
        # cur = conn.cursor()
        # sql_select_query = f"""select * from {table_name} where userid = ?"""
        # cur.execute(sql_select_query, (user_id,))
        # conn.commit()
        return cur.fetchall()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def update_data(tablet_name, new_data_name, new_data, where_name, user_id):
    try:
        # sqlite_connection = sqlite3.connect('orders.db')
        # cursor = sqlite_connection.cursor()
        # print("Подключен к SQLite")

        with sqlite3.connect(r'db/orders.db') as conn:
            cur = conn.cursor()
            sql_update_query = f"""Update {tablet_name} set {new_data_name}=? where {where_name}=?"""
            data = (new_data, user_id)
            cur.execute(sql_update_query, data)
            conn.commit()
        # conn = sqlite3.connect(r'db/orders.db', timeout=10)
        # cur = conn.cursor()
        # sql_update_query = f"""Update {tablet_name} set {new_data_name}=? where {where_name}=?"""
        # data = (new_data, user_id)
        # cur.execute(sql_update_query, data)
        # sqlite_connection.commit()
        #print("Запись успешно обновлена")
        # conn.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


# print(socket.gethostbyname(socket.gethostname()))
# insert_data([str(socket.gethostbyname(socket.gethostname())),
#              0, 0, 0,
#              0,
#              0,
#              0])
#
# print(select_all_from(str(socket.gethostbyname(socket.gethostname()))))
# update_data('x',
#             1,
#             'userid',
#             str(socket.gethostbyname(socket.gethostname())))
# print(select_all_from(str(socket.gethostbyname(socket.gethostname()))))


app = Flask(__name__)
_rotInfo, _xyz = {}, [0, 0, 0]


all_data = {}
return_data = ''


@app.route("/")
def hello():
   return "<h1 style='color:blue'>hi</h1>"


@app.route('/set_info', methods=['POST', 'GET'])
def set_info():
    global _rotInfo, _xyz, all_data

    data = request.json
    print(data)
    user_id = str(data['userid'])
    selected = select_all_from(str(data['userid']), 'users_data')

    # _xyz = data['xyz']
    # _rotInfo = data['rotInfo']

    # data = {'xyz': data['xyz'], 'speed': data['speed'], 'rot': data['rotation'], 'opened': data['opened'],
    #         "rot2": data['rotation2']}
    #
    # all_data = data
    # print('all ok')

    if len(selected):
        update_data('users_data', 'x', data['xyz'][0], 'userid', user_id)
        update_data('users_data', 'y', data['xyz'][1], 'userid', user_id)
        update_data('users_data', 'z', data['xyz'][2], 'userid', user_id)
        update_data('users_data', 'grip_open', data['opened'], 'userid', user_id)
        update_data('users_data', 'grip_rot', data['rotation'], 'userid', user_id)
        update_data('users_data', 'last_link_rot', data['rotation2'], 'userid', user_id)
        update_data('manip_data', 'speed', data['speed'], 'userid', user_id)
    else:
        insert_data([user_id,
                     data['xyz'][0],data['xyz'][1],data['xyz'][2],
                     data['opened'],
                     data['rotation'],
                     data['rotation2'],
                     data['speed']], "users_data", '(?, ?, ?, ?, ?, ?, ?, ?)')
        insert_data([user_id,0,90,90,90,90,'null',50], "manip_data", '(?, ?, ?, ?, ?, ?, ?, ?)')

    # all_data = requests.post(url, json=data)
    return 'ok'


@app.route('/set_info_manip', methods=['POST', 'GET'])
def set_info_manip():
    global _rotInfo, _xyz, all_data

    data = request.json
    #print(data)
    user_id = str(data['userid'])
    selected = select_all_from(str(data['userid']), 'manip_data')

    if len(selected):
        if data['return'] and data['return'] == 'ok':
            update_data('manip_data', 'table_rot', data['table_rot'], 'userid', user_id)
            update_data('manip_data', 'alf1', data['alf_rots'][0], 'userid', user_id)
            update_data('manip_data', 'alf2', data['alf_rots'][1], 'userid', user_id)
            update_data('manip_data', 'alf3', data['alf_rots'][2], 'userid', user_id)
            if len(data['alf_rots']) > 3:
                update_data('manip_data', 'alf4', data['alf_rots'][3], 'userid', user_id)
            update_data('manip_data', 'status', data['return'], 'userid', user_id)
        else:
            update_data('manip_data', 'status', data['return'], 'userid', user_id)
        return 'ok'
    else:
        insert_data([user_id,
                    0,0,0,
                    0,
                    0,
                    0,
                    0], "users_data")
        insert_data([user_id,data['table_rot'],
                     data['alf_rots'][0],
                     data['alf_rots'][1],
                     data['alf_rots'][2],
                     data['alf_rots'][3], 'null'], "manip_data")
        return 'ok'

    # all_data = requests.post(url, json=data)
    return 'error'


@app.route('/get_info', methods=['POST', 'GET'])
def get_info():
    global _rotInfo, _xyz, all_data

    data = request.json

    selected = select_all_from(str(data['userid']), 'users_data')
    selected_data_manip = select_all_from(str(data['userid']), 'manip_data')

    if selected_data_manip and len(selected_data_manip) == 0:
        insert_data([data['userid'],0,90,90,90,90,'null',50], "manip_data", '(?, ?, ?, ?, ?, ?, ?, ?)')

    if selected and len(selected):
        selected = selected[0]
        manip_data = selected_data_manip[0]
        return {'xyz': [selected[1],selected[2],selected[3]],
                'rot': selected[5],
                'opened': selected[4],
                "rot2": selected[6],
                'table_rot': manip_data[1],
                'alf_rots': [manip_data[2],
                             manip_data[3],
                             manip_data[4],
                             manip_data[5]],
                'status': manip_data[6],
                'speed': manip_data[7]
                }


    else:
        return '404'

    return '404'


@app.route('/get_speed', methods=['POST', 'GET'])
def get_speed():
    url = 'http://169.254.69.215:5000/get_speed'
    return_data = requests.post(url)
    #print(return_data)
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
    app.run(host="192.168.1.161",debug=True, port=5000)
