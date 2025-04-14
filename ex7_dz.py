import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

#Запрос без параметра 'method'
response = requests.get(url)
print(response.text)

# Запрос с методом HEAD
response = requests.head(url)
print(response.text)

# Запрос с правильным параметром method
params = {'method': 'POST'}
response = requests.post(url, data=params)
print(response.text)  # Выведет ответ сервера

methods = ['GET', 'POST', 'PUT', 'DELETE']

for real_method in ['GET', 'POST', 'PUT', 'DELETE']:
    for method in methods:
        params = {'method': method}

        if real_method == 'GET':
            response = requests.get(url, params=params)
        elif real_method == 'POST':
            response = requests.post(url, data=params)
        elif real_method == 'PUT':
            response = requests.put(url, data=params)
        elif real_method == 'DELETE':
            response = requests.delete(url, data=params)

        print(f"Real method: {real_method}, Method parameter: {method}")
        print("Response:", response.text)
        print("-" * 50)