import requests


class TestCheckCookies:
    def test_check(self):
        url = 'https://playground.learnqa.ru/api/homework_cookie'
        response = requests.get(url)
        cookie = dict(response.cookies)
        cookie_value = response.cookies.get('HomeWork')
        assert cookie_value == 'hw_value', "Wrong value"