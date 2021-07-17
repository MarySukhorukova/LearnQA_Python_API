import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time


class TestUserGet(BaseCase):

    def test_get_user_details_auth_as_another_user(self):
        register_data = self.prepare_registration_data()
        time.sleep(2)
        register_data2 = self.prepare_registration_data()

        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)
        response2 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data2)

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response2, 'id')
        username = register_data['username']

        login_data = {
            'email': email,
            'password': password
        }

        response3 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        response4 = requests.get(f'https://playground.learnqa.ru/api/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid})

        list_not_expected_fields = ['email', 'lastName', 'firstname', 'password']
        Assertions.assert_json_has_no_keys(response4, list_not_expected_fields)
        Assertions.assert_json_value_by_name(response4, "username", username, "username does not match")

