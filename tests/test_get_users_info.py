
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase): ##4.3
    def test_get_not_auth_user_info(self):
        url = "https://playground.learnqa.ru/api/user/2"
        response = requests.get(url)

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, 'email')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')