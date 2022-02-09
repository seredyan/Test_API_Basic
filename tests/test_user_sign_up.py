
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserSignUp(BaseCase):
    url = "/user/"

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