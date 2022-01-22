import os
import requests
import json
from datetime import datetime


def write_to_json(to_json):
    path = 'json'
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = f'{path}/{datetime.now().strftime("%d-%m-%Y--%H-%M")}-response-github.json'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(to_json, f, indent=4)


username = 'EduardMI'
response = requests.get(f'https://api.github.com/users/{username}/repos')

if response.ok:
    data = response.json()
    write_to_json(data)

    repo_name = [item['name'] for item in data]
    print(repo_name)
