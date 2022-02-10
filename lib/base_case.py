import json.decoder
import string
import random

from requests import Response
from _datetime import datetime




class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]



    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]



    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}' "

        assert name in response_as_dict, f"Response JSON has no key '{name}'"

        return response_as_dict[name]


    def prepare_signingup_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def random_username(self, prefix, maxlen):
        symbols = string.ascii_letters
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(250, maxlen))])