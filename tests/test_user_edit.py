
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    url = "https://playground.learnqa.ru/api/user/"
    url_login = "https://playground.learnqa.ru/api/user/login"

    def test_edit_just_created_user(self):

        # SIGN UP
        signingup_data = self.prepare_signingup_data()
        response1 = requests.post(self.url, data=signingup_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = signingup_data['email']
        first_name = signingup_data['firstName']
        password = signingup_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = requests.post(self.url_login, data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        url_user_id = f"https://playground.learnqa.ru/api/user/{user_id}"

        response3 = requests.put(url_user_id,
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = requests.get(url_user_id,
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )


        Assertions.assert_json_value_by_name(response4,
                                             'firstName',
                                             new_name,
                                             f"Wrong name of the user after edit. Expected: {new_name}. Actual: {response4.json()['firstName']}")















