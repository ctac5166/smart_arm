import requests


def get_server_info():
    url = 'http://192.168.0.109:5000/info/get'
    return_data = requests.get(url)
    if return_data.ok:
        return return_data.json()


def get_speed():
    url = 'http://192.168.0.109:5000/get_speed'
    return_data = requests.get(url)
    if return_data.ok:
        return return_data.json()


def set_new_pos(_xyz=[0, 0, 0]):
    url = 'http://192.168.0.109:5000/pos/set/vr'
    data = {'xyz': _xyz, "speed": 25}
    return_data = requests.post(url, json=data)
    if return_data.ok:
        return return_data


def set_new_rot(rot_info):
    url = 'http://127.0.0.1:5000/coords/rot/set'
    data = {'rotInfo': rot_info}
    return_data = requests.post(url, json=data)
    if return_data.ok:
        return return_data.json()


def set_new_pos_nativ(rot_info = [0, 0, 0, 0]):
    url = 'http://127.0.0.1:5000/coords/all/set'
    data = {'rotInfo': rot_info}
    return_data = requests.post(url, json=data)
    if return_data.ok:
        return return_data.json()


# print(get_server_info())
# x_ = 230
print(set_new_pos([0.1, 0, 0.2]))
# for i in range(50, 500):
#     if(set_new_pos([x_, 1, i]) == "tomuch") :
#         bool_exited = True
#         exit_index = 0
#         while bool_exited or exit_index>50:
#             x_ -= 1
#             if(set_new_pos([x_, 1, i]) == 'ok'): bool_exited = False
#             exit_index += 1
# # print(set_new_rot([0.5,0.5,0.5,0.5]))
# # print(set_new_pos_nativ([0.5, 0.5, 0.5, 0.5]))
print(get_server_info())


# url = 'http://192.168.0.21:8080/coords/info/get'
# data = {'xyz': [0.3, 0, 0]}
# return_data = requests.post(url, json=data)
# print(return_data)


# url = 'http://127.0.0.1:5000//coords/info/get'
# data = {'xyz': [0,0,0]}
# return_data = requests.post(url, json=data)
# if return_data.ok:
#     print (return_data.json())
