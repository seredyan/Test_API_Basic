
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):  # 4.4
    url = "/user/"
    url_login = "/user/login"

    def test_edit_just_created_user(self):

        # 1. SIGN UP
        signingup_data = self.prepare_signingup_data()
        response1 = MyRequests.post(self.url, data=signingup_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = signingup_data['email']
        first_name = signingup_data['firstName']
        password = signingup_data['password']
        user_id = self.get_json_value(response1, "id")

        # 2. LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post(self.url_login, data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # 3. EDIT
        new_name = "Changed Name"

        url_user_id = f"/user/{user_id}"

        response3 = MyRequests.put(url_user_id,
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response3, 200)

        # 4. GET
        response4 = MyRequests.get(url_user_id,
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )


        Assertions.assert_json_value_by_name(response4,
                                             'firstName',
                                             new_name,
                                             f"Wrong name of the user after edit. Expected: {new_name}. Actual: {response4.json()['firstName']}")
















