from typing import Optional
from lib.logger import Logger
import allure
import requests
from environment import ENV_OBJECT


class MyRequests:

    @staticmethod
    def post(url: str, data: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None):
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    def get(url: str, data: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "GET")

    @staticmethod
    def put(url: str, data: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
    def delete(url: str, data: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[dict] = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):
        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if data is None:
            data = {}
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == "GET":
            response = requests.get(url, headers=headers, cookies=cookies, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, cookies=cookies, data=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, cookies=cookies, data=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, cookies=cookies, data=data)
        else:
            raise Exception(f"Bad HTTP method: '{method}' was received")



        Logger.add_response(response)

        return response