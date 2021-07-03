import requests
import json
import time

response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
response_json = response.text
obj = json.loads(response_json)
token = obj['token']
seconds = obj['seconds']

response2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})
response_json2 = response2.text
obj2 = json.loads(response_json2)
status = obj2['status']
if status == 'Job is NOT ready':
    pass
else:
    print('не правильный статус')
time.sleep(seconds)

response3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})
response_json3 = response3.text
obj3 = json.loads(response_json3)
result = obj3['result']
status2 = obj3['status']
if status2 == 'Job is ready' and result != None:
    print("Don't panic! The task is done")
else:
    print('You should panic!')