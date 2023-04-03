import requests
from pprint import pprint
from datetime import datetime, timedelta
import pandas as pd

# Task 1
def compare_heroes_intelligence(*args):
    url = f'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'
    response = requests.get(url)
    all_heroes = response.json()
    user_heroes = []
    for hero in all_heroes:
        if hero['name'] in args:
            user_heroes.append((hero['name'], hero['powerstats']['intelligence']))
        if len(args) == len(user_heroes):
            break
    max_hero = max(user_heroes)
    return f'The most intelligent hero between {", ".join(args)} is {max_hero[0]} with intelligence {max_hero[1]} points'

# Task 2
class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {token}'}

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        upload_link = response.json().get('href')
        return upload_link

    def upload(self, file_path, file_name):
        href = self._get_upload_link(file_path)
        with open(file_name, 'rb') as file:
            response = requests.put(href, data=file)
        if not response.status_code == 201:
            return f'Unsuccessful result with response code: {response.status_code}'
        else:
            return 'Successfully uploaded'

# Task 3
class StackOverflow:

    def __init__(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 1)

    def get_questions_list(self, tag, last_days_period):
        api_url = 'https://api.stackexchange.com//2.3/questions?'
        todate = datetime.now().date()
        fromdate = todate - timedelta(days=last_days_period)
        params = {'fromdate': fromdate,
                  'todate': todate,
                  'order': 'asc',
                  'sort': 'creation',
                  'tagged': tag,
                  'site': 'stackoverflow'}
        response = requests.get(api_url, params=params)
        data = response.json()
        result = pd.DataFrame()
        for question in data['items']:
            creation_date = datetime.fromtimestamp(question['creation_date'])
            title = question['title']
            link = question['link']
            tags = question['tags']
            row = {'date': creation_date, 'title': title, 'link': link, 'tags': tags}
            result = pd.concat([result, pd.DataFrame([row])])
        return result.reset_index(drop=True)


if __name__ == '__main__':
    path_to_file = 'test/test123.txt'
    token = ''
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file, 'test.txt')
    print(result)

    pprint(compare_heroes_intelligence('Hulk', 'Captain America', 'Thanos'))

    stflow = StackOverflow()
    pprint(stflow.get_questions_list('python',2))
