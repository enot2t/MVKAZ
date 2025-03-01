import requests

url = 'http://numbersapi.com/43'

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print('Error')