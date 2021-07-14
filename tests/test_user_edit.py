import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):

    def test_edit_user_auth_user(self):
        # Register
        register_date = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_date)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_date['email']
        first_name = register_date['firstName']
        password = register_date['password']
        user_id = self.get_json_value(response1, 'id')

        # Auth
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)
        auth_sid = response1.cookies.get(response2, "auth_sid")
        token = response1.cookies.get(response2, "x-csrf-token")

        # Edit email
        email = 'test.com'

        response3 = MyRequests.put(f'/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid},
                                 data={'email': email})

        Assertions.assert_code_status(response3, 400)

        # Edit name

        name = 'a'
        response4 = MyRequests.put(f'/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid},
                                 data={'firstName': name})

        Assertions.assert_code_status(response4, 400)

    def test_edit_user_not_auth(self):
        name = 'Harry'
        response = MyRequests.put(f'/api/user/{user_id}',
                                 data={'firstName': name})

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == 'Auth token not supplied', f'wrong error message {response.content}'

    def test_edit_another_user_auth(self):
        name = 'Harry'
        response6 = requests.put(f'https://playground.learnqa.ru/api/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid},
                                 data={'firstName': name})

        Assertions.assert_code_status(response4, 400)
        print(response6.content)


