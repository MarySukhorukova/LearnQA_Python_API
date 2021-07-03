import requests

response1 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type')
# указан неверный метод
print(response1.status_code)
print(response1.text)

response2 = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type')
# текста ответа нет, код ответа 400
print(response2.status_code)
print(response2.text)

response3 = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data={"method": 'DELETE'})
# в случае с get, put, post код овтета 200 и success, с delete Wrong method provided и 200
print(response3.status_code)
print(response3.text)


methods_list = ["GET", "POST", "PUT", "DELETE"]

for i in methods_list:
    for x in methods_list:
        response_get = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method': i})
        print(f"Тип запроса {x}, метод {i}, код ответа {response_get.status_code}")
        if x != i and response_get.text == '{"success":"!"}':
            print(f"Тип запроса {x} не совпадает со значением параметра {i}")
        response_post = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': i})
        print(f"Тип запроса {x}, метод {i}, статус код {response_post.status_code}")
        if x != i and response_post.text == '{"success":"!"}':
            print(f"Тип запроса {x} не совпадает со значением параметра {i}")
        response_put = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': i})
        print(f"Тип запроса {x}, метод {i}, статус код {response_put.status_code}")
        if x != i and response_put.text == '{"success":"!"}':
            print("Тип запроса не совпадает со значением параметра")
        response_del = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': i})
        print(f"Тип запроса {x}, метод {i}, статус код {response_del.status_code}")
        if x != i and response_del.text == '{"success":"!"}':
            print("Тип запроса не совпадает со значением параметра")