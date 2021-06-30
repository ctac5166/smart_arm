import requests


url = 'http://127.0.0.1:5000//FlaskTutorial'
data = {'x': 0, 'y': 1, 'z': 2}
return_data = requests.post(url, json=data)
if return_data.ok:
    print (return_data.json())