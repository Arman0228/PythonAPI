import datetime
import os

from requests import Response


class Logger:
    # Путь к logger.py (C:\Users\Dastan\PythonAPI\lib)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Поднимаемся на уровень выше, чтобы попасть в корень проекта (C:\Users\Dastan\PythonAPI)
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    # Путь к logs в корне проекта
    LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
    file_name = os.path.join(LOG_DIR, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    @classmethod
    def _write_log_to_file(cls, data: str):
        # Создаём директорию logs в корне проекта, если её нет
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        with open(cls.file_name, "a", encoding="utf-8") as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        testname = os.environ.get("PYTEST_CURRENT_TEST")

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f" Request method: {method}\n"
        data_to_add += f" Request URL: {url}\n"
        data_to_add += f" Request data: {data}\n"
        data_to_add += f" Request headers: {headers}\n"
        data_to_add += f" Request cookies: {cookies}\n"
        data_to_add += f"\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response header: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += f"\n-----\n"

        cls._write_log_to_file(data_to_add)

