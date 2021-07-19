import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Editing a user cases")
class TestUserEdit(BaseCase):

    @allure.title("Register user and change fields")
    @allure.description("This test register user then auth by them and change name/email (success)")
    def test_edit_user_auth_user(self):
        # Register
        register_date = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_date)

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
        response2 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)
        auth_sid = response1.cookies.get(response2, "auth_sid")
        token = response1.cookies.get(response2, "x-csrf-token")

        # Edit email
        email = 'test.com'

        response3 = requests.put(f'https://playground.learnqa.ru/api/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid},
                                 data={'email': email})

        Assertions.assert_code_status(response3, 400)

        # Edit name

        name = 'a'
        response4 = requests.put(f'https://playground.learnqa.ru/api/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid},
                                 data={'firstName': name})

        Assertions.assert_code_status(response4, 400)

    @allure.title("Change name not authorize user")
    @allure.description("In this test user not authorize and trying change the name (not success)")
    def test_edit_user_not_auth(self):
        name = 'Harry'
        response = requests.put('https://playground.learnqa.ru/api/user/25', data={'firstName': name})

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == 'Auth token not supplied', f'wrong error message {response.content}'

    @allure.title("Editing another user")
    @allure.description("In this test user authorize and change another user (not success)")
    def test_edit_another_user_auth(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)
        auth_sid = response1.cookies.get(response1, "auth_sid")
        token = response1.cookies.get(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id") + 1
        name = 'Harry'
        response2 = requests.put(f'https://playground.learnqa.ru/api/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={"auth_sid": auth_sid},
                                 data={'firstName': name})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == 'Auth token not supplied', f'wrong error message {response2.content}'

