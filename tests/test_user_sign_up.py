import random
import string

import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserSignUp(BaseCase):
    url = "/user/"
    fields = [
        ('username'),
        ('password'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    def test_create_user_successfully(self):  #4.2
        data = self.prepare_signingup_data()

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')


    def test_create_user_with_existing_email(self): #4.1
        email = 'vinkotov@example.com'
        data = self.prepare_signingup_data(email)

        response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"



    def test_sign_up_user_with_wrong_email_format(self): # Exc 15.1
        email = 'someemailexample.com'
        data = self.prepare_signingup_data(email)

        response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"



    @pytest.mark.parametrize('field', fields)  ## Exc 15.2
    def test_missing_sign_up_field(self, field):
        data = self.prepare_signingup_data()

        del data[field]

        response = MyRequests.post(self.url, data=data)
        response_content = response.content.decode("utf-8")
        Assertions.assert_code_status(response, 400)
        assert response_content == f"The following required params are missed: {field}"



    def test_sign_up_with_too_short_username(self):  ## Exc 15.3
        data = self.prepare_signingup_data()
        data['username'] = 'a'
        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short"



    def test_too_long_username(self):  ## Exc 15.4
        data = self.prepare_signingup_data()
        data['username'] = self.random_username("user_", 255)
        # data['username'] = ''.join(random.choices(string.ascii_uppercase, k=251))

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long"

