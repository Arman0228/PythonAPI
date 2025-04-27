import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_dat()

        response = MyRequests.post("/user/", data=data)



        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_dat(email)

        response = MyRequests.post("/user/", data=data)


        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected status code {response.content} 400"

    def test_create_user_with_invalid_email(self):
        # Тест: создание пользователя с email без символа @
        data = self.prepare_registration_dat()
        data["email"] = "invalid.email.com"  # Email без @

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
    @pytest.mark.parametrize("missing_field", ["username", "firstName", "lastName", "email", "password"])
    def test_create_user_missing_field(self, missing_field):
        # Тест: создание пользователя без одного из обязательных полей
        data = self.prepare_registration_dat()
        del data[missing_field]  # Удаляем одно поле из данных

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The following required params are missed" in response.content.decode("utf-8"), f"Unexpected response content {response.content}"

    def test_create_user_with_short_name(self):
        # Тест: создание пользователя с именем длиной 1 символ
        data = self.prepare_registration_dat()
        data["firstName"] = "A"  # Имя из одного символа

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The value of 'firstName' field is too short" in response.content.decode("utf-8"), f"Unexpected response content {response.content}"

    def test_create_user_with_long_name(self):
        # Тест: создание пользователя с именем длиннее 250 символов
        long_name = "A" * 251  # Строка длиной 251 символ
        data = self.prepare_registration_dat()
        data["firstName"] = long_name

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The value of 'firstName' field is too long" in response.content.decode("utf-8"), f"Unexpected response content {response.content}"
