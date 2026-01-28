import requests
import json

url = "http://127.0.0.1:8000/names/2"  # آدرس سرور FastAPI و item_id
headers = {"Content-Type": "application/json"}
params = {"name": "ali"}  # نام جدید به عنوان پارامتر query

response = requests.delete(url, headers=headers, params=params)

if response.status_code == 202:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
