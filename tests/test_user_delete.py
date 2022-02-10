
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestDeleteUser(BaseCase):

    url_login = "/user/login"

##  Make sure the system will not let you delete this user
    def test_delete_permanent_user(self):  ## Exc 18.1

        user_id = "2"
        url_delete = f"/user/{user_id}"
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post(self.url_login, data=data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_by_name(response1,"user_id", int(user_id),
                                             f"User_id ({response1.json()['user_id']})"
                                            f" of the logged user is not equal to the required id={user_id}")


        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(url_delete, cookies={"auth_sid": auth_sid}, headers={"x-csrf-token": token})
        assert response2.text == f"Please, do not delete test users with ID 1, {user_id}, 3, 4 or 5."
        Assertions.assert_code_status(response2, 400)


    def test_create_and_delete_user(self):  ## Exc 18.2

        # SIGN UP
        data = self.prepare_signingup_data()
        url = "/user/"
        response1 = MyRequests.post(url, data=data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN
        user_id = response1.json()["id"]
        email = data['email']
        password = data['password']
        data_created_user = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post(self.url_login, data_created_user)
        Assertions.assert_code_status(response2, 200)
        print(response2.text)
        Assertions.assert_json_has_key(response2, "user_id")

        # DELETE
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        url_user = f"{url}{user_id}"

        response3 = MyRequests.delete(url_user, cookies={"auth_sid": auth_sid}, headers={"x-csrf-token": token})
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(url_user)
        assert response4.text == "User not found"



## negative test, authorized user is trying to delete an another user
    def test_auth_user_tries_delete_other_user(self): ## Exc 18.3
        url = "/user/"

        # SIGN UP USER 1
        data_user1 = self.prepare_signingup_data()
        response1 = MyRequests.post(url, data=data_user1)
        user_id_1 = response1.json()["id"]
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # SIGN UP USER 2
        data_user2 = self.prepare_signingup_data()
        response2 = MyRequests.post(url, data=data_user2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        # LOGIN USER 2
        user_id_2 = response2.json()["id"]
        email = data_user2['email']
        password = data_user2['password']
        data_created_user = {
            'email': email,
            'password': password
        }

        response3 = MyRequests.post(self.url_login, data_created_user)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "user_id")

        # USER 2 TRIES TO DELETE USER 1
        auth_sid_user_2 = self.get_cookie(response3, "auth_sid")
        token_user_2 = self.get_header(response3, "x-csrf-token")
        url_user_1 = f"{url}{user_id_1}"

        response4 = MyRequests.delete(url_user_1, cookies={"auth_sid": auth_sid_user_2}, headers={"x-csrf-token": token_user_2})
        assert response4.content.decode("utf-8") == ""