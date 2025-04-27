from lib.my_requests import MyRequests


from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': "vinkotov@example.com",
            'password': "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)


    def test_get_user_details_auth_as_different_user(self):
        # Шаг 1: Авторизация первым пользователем
        data = {
            'email': "vinkotov@example.com",
            'password': "1234"
        }
        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)  # Проверяем успешность авторизации

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # Шаг 2: Запрашиваем данные другого пользователя (например, с ID 1)
        different_user_id = 1  # Предполагаем, что это ID другого пользователя
        if different_user_id == user_id_from_auth_method:
            # Если ID совпадают, выбираем другой ID
            different_user_id = user_id_from_auth_method + 1

        response2 = MyRequests.get(
            f"/user/{different_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Шаг 3: Проверяем, что в ответе есть только username
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")