import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserRegister(BaseCase):

    def test_incorrect_email(self):
        email = 'harrypotter.gmail.com'
        data = {
            'password': '1234',
            'username': 'expelliarmus',
            'firstName': 'Harry',
            'lastName': 'Potter',
            'email': email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        print(response.status_code)
        print(response.content)