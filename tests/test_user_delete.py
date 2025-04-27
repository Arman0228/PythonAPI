import allure
import pytest
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions

@allure.epic("Delete user cases")
@allure.feature("User deletion")
class TestUserDelete(BaseCase):

    @allure.story("Protected user deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "regression", "negative")
    @allure.description("Test attempt to delete protected user with ID=2")
    def test_delete_protected_user(self):
        with allure.step("Login as protected user (ID=2)"):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response1, 200)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        with allure.step("Attempt to delete protected user"):
            response2 = MyRequests.delete(
                "/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_code_status(response2, 400)
            Assertions.assert_json_value_by_name(
                response2,
                "error",
                "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                "Unexpected response content"
            )

    @allure.story("Successful user deletion")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "regression", "positive")
    @allure.description("Test successful deletion of newly created user")
    def test_delete_just_created_user(self):
        with allure.step("Register new user"):
            register_data = self.prepare_registration_dat()
            response1 = MyRequests.post("/user", data=register_data)
            Assertions.assert_code_status(response1, 200)
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login as created user"):
            login_data = {
                'email': register_data['email'],
                'password': register_data['password']
            }
            response2 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response2, 200)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Delete user"):
            response3 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_code_status(response3, 200)

        with allure.step("Verify user is deleted"):
            response4 = MyRequests.get(f"/user/{user_id}")
            Assertions.assert_code_status(response4, 404)
            assert response4.content.decode("utf-8") == "User not found", \
                f"Unexpected response content: {response4.content}"

    @allure.story("Unauthorized user deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "regression", "negative")
    @allure.description("Test attempt to delete user by another unauthorized user")
    def test_delete_user_by_another_user(self):
        with allure.step("Register first user"):
            register_data1 = self.prepare_registration_dat()
            response1 = MyRequests.post("/user", data=register_data1)
            Assertions.assert_code_status(response1, 200)
            user_id_to_delete = self.get_json_value(response1, "id")

        with allure.step("Register second user"):
            register_data2 = self.prepare_registration_dat()
            response2 = MyRequests.post("/user", data=register_data2)
            Assertions.assert_code_status(response2, 200)

        with allure.step("Login as second user"):
            login_data2 = {
                'email': register_data2['email'],
                'password': register_data2['password']
            }
            response3 = MyRequests.post("/user/login", data=login_data2)
            Assertions.assert_code_status(response3, 200)

            auth_sid2 = self.get_cookie(response3, "auth_sid")
            token2 = self.get_header(response3, "x-csrf-token")

        with allure.step("Attempt to delete first user by second user"):
            response4 = MyRequests.delete(
                f"/user/{user_id_to_delete}",
                headers={"x-csrf-token": token2},
                cookies={"auth_sid": auth_sid2}
            )

        with allure.step("Verify first user still exists"):
            login_data1 = {
                'email': register_data1['email'],
                'password': register_data1['password']
            }
            response5 = MyRequests.post("/user/login", data=login_data1)
            Assertions.assert_code_status(response5, 200)

            auth_sid1 = self.get_cookie(response5, "auth_sid")
            token1 = self.get_header(response5, "x-csrf-token")
            response6 = MyRequests.get(
                f"/user/{user_id_to_delete}",
                headers={"x-csrf-token": token1},
                cookies={"auth_sid": auth_sid1}
            )
            Assertions.assert_json_has_key(response6, "username")