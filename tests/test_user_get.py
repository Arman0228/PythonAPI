from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User data access")
@allure.feature("User details retrieval")
class TestUserGet(BaseCase):

    @allure.story("Unauthorized access")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    @allure.description("Test that unauthorized user can only see username")
    def test_get_user_details_not_auth(self):
        with allure.step("Get user details without authorization"):
            response = MyRequests.get("/user/2")

        with allure.step("Verify only username is visible"):
            Assertions.assert_json_has_key(response, "username")
            Assertions.assert_json_has_not_key(response, "email")
            Assertions.assert_json_has_not_key(response, "firstName")
            Assertions.assert_json_has_not_key(response, "lastName")

    @allure.story("Authorized access")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "positive")
    @allure.description("Test that authorized user can see all own details")
    def test_get_user_details_auth_as_same_user(self):
        with allure.step("Login as test user"):
            data = {
                'email': "vinkotov@example.com",
                'password': "1234"
            }
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Get own user details"):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step("Verify all fields are visible"):
            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.story("Cross-user access")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    @allure.description("Test that user can't see private details of another user")
    def test_get_user_details_auth_as_different_user(self):
        with allure.step("Login as first user"):
            data = {
                'email': "vinkotov@example.com",
                'password': "1234"
            }
            response1 = MyRequests.post("/user/login", data=data)
            Assertions.assert_code_status(response1, 200)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Attempt to get different user details"):
            different_user_id = 1
            if different_user_id == user_id_from_auth_method:
                different_user_id = user_id_from_auth_method + 1

            response2 = MyRequests.get(
                f"/user/{different_user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        with allure.step("Verify only public fields are visible"):
            Assertions.assert_json_has_key(response2, "username")
            Assertions.assert_json_has_not_key(response2, "email")
            Assertions.assert_json_has_not_key(response2, "firstName")
            Assertions.assert_json_has_not_key(response2, "lastName")