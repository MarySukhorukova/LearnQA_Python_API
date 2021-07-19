import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import allure
from lib.methods import generate_random_string


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    params = [
    ({'password': '1234', 'username': 'qwerty', 'firstName': 'Qwe', 'lastName': 'Rty'}, 'email'),
    ({'username': 'qwerty', 'firstName': 'Qwe', 'lastName': 'Rty', 'email': 'test@example.com'}, 'password'),
    ({'password': 'qwerty', 'firstName': 'Qwe', 'lastName': 'Rty', 'email': 'test@example.com'}, 'username'),
    ({'password': 'qwerty', 'username': 'test', 'lastName': 'Rty', 'email': 'test@example.com'}, 'firstName'),
    ({'password': 'qwerty', 'username': 'test', 'firstName': 'Qwe', 'email': 'test@example.com'}, 'lastName')
    ]

    def setup(self):
        base_part = 'learnqa'
        domain = '@example.com'
        random_part = datetime.now().strftime('%m%d%Y%H%M%S')
        self.email = f'{base_part}{random_part}{domain}'
        self.incorrect_email = f'{base_part}{random_part}'

    @allure.title("Register with incorrect email")
    @allure.description("In this test user register without @ in email (not success)")
    def test_create_user_incorrect_email(self):
        data = {
            'password': '1234',
            'username': 'expelliarmus',
            'firstName': 'Harry',
            'lastName': 'Potter',
            'email': self.incorrect_email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == 'Invalid email format', f'wrong error message {response.content}'

    @allure.title("Register with short name")
    @allure.description("In this test user register with short name - one letter (not success)")
    def test_create_user_with_short_name(self):
        data = {
            'password': '1234',
            'username': 'expelliarmus',
            'firstName': generate_random_string(1),
            'lastName': 'Potter',
            'email': self.email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", \
            f'wrong error message {response.content}'

    @allure.title("Register with long name")
    @allure.description("In this test user register with long name - over 256 letters (not success)")
    def test_create_user_with_long_name(self):
        data = {
            'password': '1234',
            'username': 'expelliarmus',
            'firstName': generate_random_string(256),
            'lastName': 'Potter',
            'email': self.email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too long", \
            f'wrong error message {response.content}'

    @allure.title("Register without required fields")
    @allure.description("In this parametrize test user try to register without required fields (not success)")
    @pytest.mark.parametrize("param", params)
    def test_create_user_without_fields(self, param):
        data, lost_parameter = param
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {lost_parameter}"





