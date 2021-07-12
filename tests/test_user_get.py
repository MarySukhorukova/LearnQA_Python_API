import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):

    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        auth_sid = response1.cookies.get(response1, "auth_sid")
        token = response1.cookies.get(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id") + 1

        response2 = requests.get(f'https://playground.learnqa.ru/api/user/{user_id_from_auth_method}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid})

        list_not_expected_fields = ['email', 'lastName', 'firstname', 'password']
        Assertions.assert_json_has_no_keys(response1, list_not_expected_fields)

