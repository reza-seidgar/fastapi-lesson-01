import requests
import json

url = "http://127.0.0.1:8000/names"
headers = {"Content-Type": "application/json"}
params = {"name": "amir"}  # نام مورد نظر به عنوان پارامتر query

response = requests.post(url, headers=headers, params=params)

if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
