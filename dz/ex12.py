import requests


def test_homework_header():
    url = "https://playground.learnqa.ru/api/homework_header"

    # Делаем GET-запрос
    response = requests.get(url)

    # Печатаем все заголовки для анализа
    print("\nResponse headers:", response.headers)

    # Проверяем наличие нужного заголовка (например, 'x-secret-homework-header')
    header_name = 'x-secret-homework-header'
    assert header_name in response.headers, f"Header '{header_name}' not found in response"

    # Получаем значение заголовка
    header_value = response.headers.get(header_name)
    print(f"Value of '{header_name}':", header_value)

    # Проверяем его значение (замените 'expected_value' на реальное ожидаемое значение)
    expected_value = 'Some secret value'  # Замените на фактическое значение из вывода print
    assert header_value == expected_value, f"Header value is not as expected. Actual: '{header_value}', Expected: '{expected_value}'"