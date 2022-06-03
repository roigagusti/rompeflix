import requests
import json

response_API = requests.get('https://www.askpython.com/', headers={'User-Agent': 'Mozilla/5.0'})
data = response_API.text
json.loads(data)