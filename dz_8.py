import requests
import time

# Шаг 1: Создаем задачу
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
data = response.json()
token = data["token"]
seconds = data["seconds"]
print(f"Задача создана. Токен: {token}, Время ожидания: {seconds} секунд")

# Шаг 2: Запрос до готовности задачи
response = requests.get(f"https://playground.learnqa.ru/ajax/api/longtime_job?token={token}")
data = response.json()
assert data["status"] == "Job is NOT ready", f"Ожидался статус 'Job is NOT ready', получен: {data['status']}"
print("Статус до готовности верный: Job is NOT ready")

# Шаг 3: Ждем указанное время
time.sleep(seconds)

# Шаг 4: Запрос после готовности задачи
response = requests.get(f"https://playground.learnqa.ru/ajax/api/longtime_job?token={token}")
data = response.json()
assert data["status"] == "Job is ready", f"Ожидался статус 'Job is ready', получен: {data['status']}"
assert "result" in data, "Поле 'result' отсутствует в ответе"
print("Статус после готовности верный: Job is ready, результат получен")