import requests


def test_check_cookie():
    # Делаем GET-запрос к API
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

    # Извлекаем cookies из ответа
    cookies = response.cookies

    # Выводим все cookies для отладки
    print("\nCookies received:", cookies)

    # Проверяем, что cookies не пустые
    assert cookies, "No cookies received in the response"

    # Ожидаемое имя cookie (например, 'HomeWork') и его значение (например, 'hw_value')
    expected_cookie_name = "HomeWork"
    expected_cookie_value = "hw_value"

    # Проверяем, что ожидаемая cookie присутствует в ответе
    assert expected_cookie_name in cookies, f"Cookie '{expected_cookie_name}' is not present in the response"

    # Получаем значение cookie
    actual_cookie_value = cookies.get(expected_cookie_name)

    # Выводим значение cookie для отладки
    print(f"\nValue of cookie '{expected_cookie_name}': {actual_cookie_value}")

    # Проверяем, что значение cookie соответствует ожидаемому
    assert actual_cookie_value == expected_cookie_value, (
        f"Unexpected value for cookie '{expected_cookie_name}'. "
        f"Expected: '{expected_cookie_value}', but got: '{actual_cookie_value}'"
    )