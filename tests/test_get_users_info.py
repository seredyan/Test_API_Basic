
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):   ##4.3
    def test_get_info_not_auth_user(self):
        url = "/user/2"

        response = MyRequests.get(url)

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, 'email')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')



    def test_get_info_same_auth_user(self):
        url_login = "/user/login"

        data = {
            'email' : 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post(url_login, data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        url_user_id = f"/user/{user_id_from_auth_method}"

        response2 = MyRequests.get(url_user_id,
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        print(response2.text)
        expected_names=['username', 'email', 'firstName', 'lastName']

        Assertions.assert_json_has_several_keys(response2, expected_names)
