import requests


def get_server_info():
    url = 'http://127.0.0.1:5000//coords/info/get'
    return_data = requests.get(url)
    if return_data.ok:
        return return_data.json()


def set_new_pos(_xyz=[0, 0, 0]):
    url = 'http://127.0.0.1:5000//coords/pos/set'
    data = {'xyz': _xyz}
    return_data = requests.post(url, json=data)
    if return_data.ok:
        return return_data.json()


def set_new_rot(_rotInfo):
    url = 'http://127.0.0.1:5000//coords/rot/set'
    data = {'rotInfo': _rotInfo}
    return_data = requests.post(url, json=data)
    if return_data.ok:
        return return_data.json()


print(get_server_info())
print(set_new_pos([2, 1, 1]))
print(set_new_rot([0.5,0.5,0.5,0.5]))
print(get_server_info())

# url = 'http://127.0.0.1:5000//coords/info/get'
# data = {'xyz': [0,0,0]}
# return_data = requests.post(url, json=data)
# if return_data.ok:
#     print (return_data.json())
