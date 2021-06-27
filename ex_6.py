import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
all_responses = response.history
last_response = response.history[-1]
print(len(all_responses))
print(last_response.url)