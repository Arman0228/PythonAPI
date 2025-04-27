import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User management")
@allure.feature("User editing")
class TestUserEdit(BaseCase):

    @allure.story("Positive edit scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test for editing just created user with valid data")
    @allure.tag("smoke", "regression", "positive")
    def test_edit_just_created_user(self):
        with allure.step("Register new user"):
            register_data = self.prepare_registration_dat()
            response1 = MyRequests.post("/user", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")
            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login as created user"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Edit user data"):
            new_name = "Changed Name"
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )
            Assertions.assert_code_status(response3, 200)

        with allure.step("Verify changes"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "First name was not changed"
            )

    @allure.story("Security tests")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Test unauthorized user edit attempt")
    @allure.tag("security", "regression", "negative")
    def test_edit_user_unauthorized(self):
        with allure.step("Register new user"):
            register_data = self.prepare_registration_dat()
            response1 = MyRequests.post("/user", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login (for verification only)"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response2, 200)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Attempt unauthorized edit"):
            new_name = "Unauthorized Change"
            response3 = MyRequests.put(
                f"/user/{user_id}",
                data={"firstName": new_name}
            )
            Assertions.assert_code_status(response3, 400)

        with allure.step("Verify no changes were made"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                register_data['firstName'],
                "First name was changed despite unauthorized access"
            )

    @allure.story("Security tests")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Test edit user as different user")
    @allure.tag("security", "regression", "negative")

    def test_edit_user_as_different_user(self):
        with allure.step("Register first user"):
            register_data1 = self.prepare_registration_dat()
            response1 = MyRequests.post("/user", data=register_data1)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id_to_edit = self.get_json_value(response1, "id")
            email1 = register_data1['email']
            password1 = register_data1['password']

        with allure.step("Login as first user (for verification)"):
            login_data1 = {
                'email': email1,
                'password': password1
            }
            response2 = MyRequests.post("/user/login", data=login_data1)
            Assertions.assert_code_status(response2, 200)

            auth_sid1 = self.get_cookie(response2, "auth_sid")
            token1 = self.get_header(response2, "x-csrf-token")

        with allure.step("Register second user"):
            register_data2 = self.prepare_registration_dat()
            response3 = MyRequests.post("/user", data=register_data2)
            Assertions.assert_code_status(response3, 200)
            Assertions.assert_json_has_key(response3, "id")

            email2 = register_data2['email']
            password2 = register_data2['password']

        with allure.step("Login as second user"):
            login_data2 = {
                'email': email2,
                'password': password2
            }
            response4 = MyRequests.post("/user/login", data=login_data2)
            Assertions.assert_code_status(response4, 200)

            auth_sid2 = self.get_cookie(response4, "auth_sid")
            token2 = self.get_header(response4, "x-csrf-token")

        with allure.step("Attempt edit first user as second user"):
            new_name = "Changed By Other User"
            response5 = MyRequests.put(
                f"/user/{user_id_to_edit}",
                headers={"x-csrf-token": token2},
                cookies={"auth_sid": auth_sid2},
                data={"firstName": new_name}
            )
            assert response5.status_code in (200, 400, 403), \
                f"Unexpected status code! Expected: 400 or 403, Actual: {response5.status_code}"

        with allure.step("Verify no changes were made"):
            response6 = MyRequests.get(
                f"/user/{user_id_to_edit}",
                headers={"x-csrf-token": token1},
                cookies={"auth_sid": auth_sid1}
            )
            Assertions.assert_json_value_by_name(
                response6,
                "firstName",
                register_data1['firstName'],
                "First name was changed by another user"
            )

    @allure.story("Validation tests")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test edit with invalid email format")
    @allure.tag("validation", "regression", "negative")

    def test_edit_email_invalid_format(self):
        with allure.step("Register new user"):
            register_data = self.prepare_registration_dat()
            response1 = MyRequests.post("/user", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response2, 200)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Attempt edit with invalid email"):
            invalid_email = "invalid.email.com"
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": invalid_email}
            )
            Assertions.assert_code_status(response3, 400)

        with allure.step("Verify no changes were made"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_json_value_by_name(
                response4,
                "email",
                email,
                "Email was changed to invalid format"
            )

    @allure.story("Validation tests")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test edit with too short first name")
    @allure.tag("validation", "regression", "negative")
    def test_edit_firstname_too_short(self):
        with allure.step("Register new user"):
            register_data = self.prepare_registration_dat()
            response1 = MyRequests.post("/user", data=register_data)
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response2, 200)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Attempt edit with too short first name"):
            short_name = "A"
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": short_name}
            )
            Assertions.assert_code_status(response3, 400)

        with allure.step("Verify no changes were made"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                register_data['firstName'],
                "First name was changed to too short value"
            )