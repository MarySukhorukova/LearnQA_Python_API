import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

from lib.methods import generate_random_string


class TestUserRegister(BaseCase):
    def setup(self):
        base_part = 'learnqa'
        domain = '@example.com'
        random_part = datetime.now().strftime('%m%d%Y%H%M%S')
        self.email = f'{base_part}{random_part}{domain}'
        self.incorrect_email = f'{base_part}{random_part}'

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

    def test_create_user_without_any_field(self):
        data_without_email = {'password': '1234', 'username': 'qwerty', 'firstName': 'Qwe', 'lastName': 'Rty'}
        data_without_pass = {'username': 'qwerty', 'firstName': 'Qwe', 'lastName': 'Rty', 'email': self.email}
        data_without_username = {'password': 'qwerty', 'firstName': 'Qwe', 'lastName': 'Rty', 'email': self.email}
        data_without_first_name = {'password': 'qwerty', 'username': 'test', 'lastName': 'Rty', 'email': self.email}
        data_without_last_name = {'password': 'qwerty', 'username': 'test', 'firstName': 'Qwe', 'email': self.email}
        list_of_data = [data_without_last_name, data_without_email,
                        data_without_pass, data_without_username, data_without_first_name]
        for i in list_of_data:
            response = requests.post('https://playground.learnqa.ru/api/user/', data=i)
            Assertions.assert_code_status(response, 400)
            print(response.content)


