from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}' "

        assert name in response_as_dict, f"Response JSON has no key '{name}'"
        assert response_as_dict[name] == expected_value, error_message


    @staticmethod
    def assert_json_has_key(response: Response, name): #4.2
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}' "

        assert name in response_as_dict, f"Response JSON has no key '{name}'"


    @staticmethod
    def assert_json_has_several_keys(response: Response, names: list):  # 4.3
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}' "

        for name in names:
            assert name in response_as_dict, f"Response JSON has no key '{name}'"


    @staticmethod
    def assert_json_has_no_key(response: Response, name):  # 4.2
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not a JSON format. Response text is '{response.text}' "

        assert name not in response_as_dict, f"Response JSON should NOT have key '{name}'. But it's present"


    @staticmethod
    def assert_code_status(response: Response, expeted_status_code): #4.2
        assert response.status_code == expeted_status_code,\
            f"Unexpected status code! Expected: {expeted_status_code}. Actual:{response.status_code}"