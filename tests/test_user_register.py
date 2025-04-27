import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User registration")
@allure.feature("User creation")
class TestUserRegister(BaseCase):

    @allure.story("Successful registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "positive")
    @allure.description("Test successful user registration with valid data")
    def test_create_user_successfully(self):
        with allure.step("Prepare registration data"):
            data = self.prepare_registration_dat()

        with allure.step("Register new user"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Verify successful registration"):
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

    @allure.story("Duplicate registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("negative")
    @allure.description("Test registration with existing email")
    def test_create_user_with_existing_email(self):
        with allure.step("Prepare registration data with existing email"):
            email = "vinkotov@example.com"
            data = self.prepare_registration_dat(email)

        with allure.step("Attempt registration"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Verify duplicate registration fails"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
                f"Unexpected status code {response.content} 400"

    @allure.story("Invalid data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "negative")
    @allure.description("Test registration with invalid email format")
    def test_create_user_with_invalid_email(self):
        with allure.step("Prepare registration data with invalid email"):
            data = self.prepare_registration_dat()
            data["email"] = "invalid.email.com"

        with allure.step("Attempt registration"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Verify registration fails"):
            Assertions.assert_code_status(response, 400)

    @allure.story("Missing required fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("validation", "negative")
    @allure.description("Test registration with missing required fields")
    @pytest.mark.parametrize("missing_field", ["username", "firstName", "lastName", "email", "password"])
    def test_create_user_missing_field(self, missing_field):
        with allure.step(f"Prepare registration data without {missing_field}"):
            data = self.prepare_registration_dat()
            del data[missing_field]

        with allure.step("Attempt registration"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Verify registration fails"):
            Assertions.assert_code_status(response, 400)
            assert "The following required params are missed" in response.content.decode("utf-8"), \
                f"Unexpected response content {response.content}"

    @allure.story("Validation - short name")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "negative")
    @allure.description("Test registration with too short first name")
    def test_create_user_with_short_name(self):
        with allure.step("Prepare registration data with short name"):
            data = self.prepare_registration_dat()
            data["firstName"] = "A"

        with allure.step("Attempt registration"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Verify registration fails"):
            Assertions.assert_code_status(response, 400)
            assert "The value of 'firstName' field is too short" in response.content.decode("utf-8"), \
                f"Unexpected response content {response.content}"

    @allure.story("Validation - long name")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "negative")
    @allure.description("Test registration with too long first name")
    def test_create_user_with_long_name(self):
        with allure.step("Prepare registration data with long name"):
            long_name = "A" * 251
            data = self.prepare_registration_dat()
            data["firstName"] = long_name

        with allure.step("Attempt registration"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Verify registration fails"):
            Assertions.assert_code_status(response, 400)
            assert "The value of 'firstName' field is too long" in response.content.decode("utf-8"), \
                f"Unexpected response content {response.content}"