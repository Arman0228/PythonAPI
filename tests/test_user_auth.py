import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
@allure.feature("User authentication")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie", allure.severity_level.NORMAL),
        ("no_token", allure.severity_level.NORMAL)
    ]

    @allure.step("Setup: authenticate test user")
    def setup_method(self, method):
        with allure.step("Authenticate with valid credentials"):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=data)
            self.auth_sid = self.get_cookie(response1, "auth_sid")
            self.token = self.get_header(response1, "x-csrf-token")
            self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.story("Successful authentication")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "positive", "authentication")
    @allure.description("This test successfully authorize user by email and password")
    def test_auth_user(self):
        with allure.step("Make authenticated request"):
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )

        with allure.step("Verify user ID matches authenticated user"):
            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                self.user_id_from_auth_method,
                "User id from auth method is not equal to user id from check method"
            )

    @allure.story("Negative authentication scenarios")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative", "authentication")
    @allure.description("This test checks authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition,severity', exclude_params)
    def test_negative_auth_check(self, condition, severity):
        with allure.step(f"Make request without {condition.replace('_', ' ')}"):
            if condition == "no_cookie":
                response2 = MyRequests.get(
                    "/user/auth",
                    headers={"x-csrf-token": self.token}
                )
            else:
                response2 = MyRequests.get(
                    "/user/auth",
                    cookies={"auth_sid": self.auth_sid}
                )

        with allure.step(f"Verify unauthorized status for {condition}"):
            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                0,
                f"User is authorized with condition {condition}"
            )