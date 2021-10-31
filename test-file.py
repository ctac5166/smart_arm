# import sqlite3
# import socket
#
#
# conn = sqlite3.connect(r'db/orders.db')
# cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS users_data(
#    userid TEXT PRIMARY KEY,
#    x REAL,
#    y REAL,
#    z REAL,
#    grip_open REAL,
#    grip_rot REAL,
#    last_link_rot REAL
#    );
# """)
# conn.commit()
#
#
# def insert_data(user):
#     try:
#         cur.execute("INSERT INTO users_data VALUES(?, ?, ?, ?, ?, ?, ?);", user)
#         conn.commit()
#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#
# def select_all_from(user_id):
#     try:
#         sql_select_query = """select * from users_data where userid = ?"""
#         cur.execute(sql_select_query, (user_id,))
#         return cur.fetchall()
#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#
# def update_data(new_data_name, new_data, where_name, user_id):
#     try:
#         # sqlite_connection = sqlite3.connect('orders.db')
#         # cursor = sqlite_connection.cursor()
#         # print("Подключен к SQLite")
#
#         sql_update_query = f"""Update users_data set {new_data_name} = ? where {where_name} = ?"""
#         data = (new_data, user_id)
#         cur.execute(sql_update_query, data)
#         # sqlite_connection.commit()
#         print("Запись успешно обновлена")
#         # cur.close()
#
#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#
#
# # print(socket.gethostbyname(socket.gethostname()))
# # insert_data([str(socket.gethostbyname(socket.gethostname())),
# #              0, 0, 0,
# #              0,
# #              0,
# #              0])
# #
# # print(select_all_from(str(socket.gethostbyname(socket.gethostname()))))
# # update_data('x',
# #             1,
# #             'userid',
# #             str(socket.gethostbyname(socket.gethostname())))
# print(select_all_from(str(socket.gethostbyname(socket.gethostname()))))
# if len(select_all_from(str(socket.gethostbyname(socket.gethostname())))):
#     print('a')
# else:
#     print('b')
#
# # print(select_all_from(''))
# import requests
# #
# # url = 'http://192.168.1.161:5000//get_info'
# # data = {'userid': '0.0.0.0'}
# # return_data = requests.post(url, json=data, verify=True)
# # if return_data.ok:
# #     data_json = return_data.json()
# #     print(data_json)
import math as m

l1 = 0.17
l2 = 0.2
l3 = 0.135
l4 = 0.205
# l4 = 0.16

a1=0
a2=30
a3=30

alf1=a1*m.pi/180
alf2=a2*m.pi/180
alf3=a3*m.pi/180

x_targ = 0.3
z_targ = 0.03



def OZK_2(x,y,z):
    a1 = m.atan(y / x)
    a5 = a1
    k = m.sqrt(x ** 2 + y ** 2)
    zp = z + l4 - l1
    d = m.sqrt(k ** 2 + zp ** 2)
    a2 = (m.pi / 2) - (m.atan(zp / k) + m.acos((d ** 2 + l2 ** 2 - l3 ** 2) / (2 * d * l2)))
    a3 = m.pi - m.acos((-d ** 2 + l2 ** 2 + l3 ** 2) / (2 * l2 * l3))
    a4 = m.pi - (a2 + a3)

    return a1, a2, a3, a4

    # return 0, Q1, Q2, 0

pos = [0,0,0]

while pos[2] < 2:
    while pos[0]  < 2:
        while pos[1] < 2:
            try:
                print(OZK_2(pos[0],pos[1],pos[2]), pos)
                pos[1] = 2
            except Exception:
                pos[1] += 0.005
        pos[1] = 0
        pos[0] += 0.005
    pos[0] = 0
    pos[1] = 0
    pos[2] += 0.005