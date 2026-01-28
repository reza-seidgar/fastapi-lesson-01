import requests
import json

url = "http://127.0.0.1:8000/names/4"  # آدرس سرور FastAPI و item_id
headers = {"Content-Type": "application/json"}
params = {"name": "ali"}  # نام جدید به عنوان پارامتر query

response = requests.put(url, headers=headers, params=params)

if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
