import requests


class TestCheckHeaders:
    def test_check(self):
        url = 'https://playground.learnqa.ru/api/homework_header'
        response = requests.get(url)
        header = dict(response.headers)
        header_value = response.headers.get('x-secret-homework-header')
        assert header_value == 'Some secret value', "Wrong value of header"
