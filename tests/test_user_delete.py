import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time


class TestUserDelete(BaseCase):

    def test_delete_user_id2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)
        auth_sid = response1.cookies.get(response1, "auth_sid")
        token = response1.cookies.get(response1, "x-csrf-token")
        response = requests.delete('https://playground.learnqa.ru/api/user/2', headers={'x-csrf-token': token},
                                    cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == 'Auth token not supplied', f'wrong error message {response.content}'

    def test_create_and_delete_user(self):
        register_date = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_date)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')
        email = register_date['email']
        password = register_date['password']
        user_id = self.get_json_value(response1, 'id')

        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

        response3 = requests.delete(f'https://playground.learnqa.ru/api/user/{user_id}', headers={'x-csrf-token': self.token},
                                    cookies={"auth_sid": self.auth_sid})

        Assertions.assert_code_status(response3, 200)

        response4 = requests.get(f'https://playground.learnqa.ru/api/user/{user_id}',
                                 headers={'x-csrf-token': self.token},
                                 cookies={"auth_sid": self.auth_sid})
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == 'User not found', f'wrong error message {response4.content}'

    def test_delete_user_when_login_another_user(self):
        register_data = self.prepare_registration_data()
        time.sleep(2)
        register_data2 = self.prepare_registration_data()

        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)
        response2 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data2)

        email = register_data['email']
        password = register_data['password']
        username = register_data['username']
        user_id = self.get_json_value(response2, 'id')

        login_data = {
            'email': email,
            'password': password
        }

        response3 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        response4 = requests.delete(f'https://playground.learnqa.ru/api/user/{user_id}',
                                    headers={'x-csrf-token': token},
                                    cookies={"auth_sid": auth_sid})

        response5 = requests.get(f'https://playground.learnqa.ru/api/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_value_by_name(response5, "username", username, "username does not match")
