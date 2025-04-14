import requests


response1 = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(f"Количество редиректов: {len(response1.history)}")

final_url = response1.url

print(f"Конечный URL: {final_url}")