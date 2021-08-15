import json
import time
import requests
from decouple import config


class DataManager:
    def __init__(self, token, name=None, account=None, type=None):
        self.name = name
        self.token = token
        self.account = account
        self.type = type
        self.users = None
        self.user_groups = None
        self.uploads = None
        self.medias = None
        self.media_category = None
        self.players = None
        self.playlists = None
        self.templates = None
        self.news = None
        self.newsources = None
        self.videowall = None
        self.reports = None

    def get_all(self, resource, payload={}):
        allResources = list()
        count = 0
        i, limit = 1, 1
        while i <= limit:
            url = f'https://api.4yousee.com.br/v1/{resource}?page={i}'
            headers = {
                'Secret-Token': self.token,
                'Content-Type': 'application/json'
            }
            time.sleep(1)
            response = requests.request("GET", url, headers=headers, params=payload)
            data = json.loads(response.text)
            print('coletando...{}'.format(resource))
            # data = json.dumps(data, indent=2)
            if data.get('totalPages', False):
                limit = data['totalPages']
                for item in data['results']:
                    allResources.append(item)
                    count += 1
                    # print(count, medias)
                i += 1
            else:
                break
        return allResources

    def get_medias(self):
        self.medias = self.get_all('medias')

    def get_media_category(self):
        self.media_category = self.get_all('medias/categories')

    def get_players(self):
        self.players = self.get_all('players')

    def get_playlists(self):
        self.playlists = self.get_all('playlists')

    def get_reports(self):
        self.reports = self.get_all('reports')


if __name__ == '__main__':
    cliente = DataManager(token='')
    # cliente.get_medias()
    # cliente.get_playlists()
    cliente.get_players()
    # cliente.get_media_category()
    # print(cliente.medias)
    # print(cliente.playlists)
    print(cliente.players)
    # print(cliente.media_category)
