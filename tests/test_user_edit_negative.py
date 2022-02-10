import random

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class Test_negative_edit_user(BaseCase): ## Ex17

    def setup(self):
        self.url = "/user/"
        self.url_login = "/user/login"

        # 1. SIGN UP
        signingup_data = self.prepare_signingup_data()
        response1 = MyRequests.post(self.url, data=signingup_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        self.email = signingup_data['email']
        self.first_name = signingup_data['firstName']
        self.password = signingup_data['password']
        self.user_id = self.get_json_value(response1, "id")


## trying to change user data while being unauthorized
    def test_edit_not_authorized_user(self):  ## Exc 17.1

        # EDIT
        new_name = "Changed Name"
        url_user_id = f"{self.url}{self.user_id}"

        response2 = MyRequests.put(url_user_id, data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Auth token not supplied"


## trying to edit user data while being authorized by another user
    def test_edit_user_by_auth_other_user(self): ## Exc 17.2

        # DATA USER 1
        email = 'yahoo123@example.com'
        data = {
            'email': email,
            'password': '1234'
        }
        # LOGIN USER 1
        response2 = MyRequests.post(self.url_login, data=data)  ## loging by USER-1{"user_id":25325}
        # print(response2.text)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        # LOGGED USER 1 TRIES TO EDIT USER 2
        new_name = "Changed Name"
        user_id = 25326
        url_user_id = f"{self.url}{user_id}"

        response3 = MyRequests.put(url_user_id,              ## attempt to edit by USER-2{"user_id":25326}
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode("utf-8") == ""

## being authorized as the same user try to edit the user's email to a new email without the @ symbol
    def test_edit_authorized_user_email_to_wrong_format(self):  ## Exc 17.3

            # LOGIN
        response1 = MyRequests.post(self.url_login, data={'email': self.email, 'password': self.password})
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

            # EDIT
        url_auth_user = self.url+self.user_id
        response2 = MyRequests.put(url_auth_user, cookies={"auth_sid": auth_sid}, headers={"x-csrf-token": token}, data={'email': self.email.replace('@',"_")})
        Assertions.assert_code_status(response2, 400)
        assert response2.text == "Invalid email format", "Unexpected response text for invalid email"



## being authorized as the same user try to edit the user's firstName to a very short value of one character
    def test_edit_user_firstname_to_too_short_name(self):  ## Exc 17.4
        # LOGIN
        response2 = MyRequests.post(self.url_login, data={'email': self.email, 'password': self.password})
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        url_auth_user = f"{self.url}{self.user_id}"
        response2 = MyRequests.put(url_auth_user, cookies={"auth_sid": auth_sid}, headers={"x-csrf-token": token},
                                 data={'firstName': random.choice(['R', 'A', 'D', '1', '$'])})
        Assertions.assert_code_status(response2, 400)
        error_message = "Too short value for field firstName"

        assert error_message in response2.text