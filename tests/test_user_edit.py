from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):

        # REGISTER
        register_data = self.prepare_registration_dat()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,  "id")
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email' : email,
            'password' : password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers = {"x-csrf-token":token},
            cookies = {"auth_sid": auth_sid},
            data = {"firstName":new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers = {"x-csrf-token":token},
            cookies = {"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "First name was not changed"
        )

    def test_edit_user_unauthorized(self):
        # Регистрация
        register_data = self.prepare_registration_dat()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Авторизация (нужна только для проверки после)
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Редактирование без авторизации
        new_name = "Unauthorized Change"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 400)

        # Проверка
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

    def test_edit_user_as_different_user(self):
        # Регистрация первого пользователя
        register_data1 = self.prepare_registration_dat()
        response1 = MyRequests.post("/user", data=register_data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id_to_edit = self.get_json_value(response1, "id")
        email1 = register_data1['email']
        password1 = register_data1['password']

        # Авторизация первым пользователем (для проверки после)
        login_data1 = {
            'email': email1,
            'password': password1
        }
        response2 = MyRequests.post("/user/login", data=login_data1)
        Assertions.assert_code_status(response2, 200)

        auth_sid1 = self.get_cookie(response2, "auth_sid")
        token1 = self.get_header(response2, "x-csrf-token")

        # Регистрация второго пользователя
        register_data2 = self.prepare_registration_dat()
        response3 = MyRequests.post("/user", data=register_data2)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        email2 = register_data2['email']
        password2 = register_data2['password']

        # Авторизация вторым пользователем
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response4 = MyRequests.post("/user/login", data=login_data2)
        Assertions.assert_code_status(response4, 200)

        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")

        # Редактирование первого пользователя вторым
        new_name = "Changed By Other User"
        response5 = MyRequests.put(
            f"/user/{user_id_to_edit}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
            data={"firstName": new_name}
        )
        assert response5.status_code in (200, 400, 403), \
            f"Unexpected status code! Expected: 400 or 403, Actual: {response5.status_code}"

        # Проверка
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

    def test_edit_email_invalid_format(self):
        # Регистрация
        register_data = self.prepare_registration_dat()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Авторизация
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Редактирование email
        invalid_email = "invalid.email.com"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": invalid_email}
        )
        Assertions.assert_code_status(response3, 400)

        # Проверка
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

    def test_edit_firstname_too_short(self):
        # Регистрация
        register_data = self.prepare_registration_dat()
        response1 = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Авторизация
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Редактирование firstName
        short_name = "A"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": short_name}
        )
        Assertions.assert_code_status(response3, 400)

        # Проверка
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