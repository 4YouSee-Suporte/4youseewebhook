from webhook.manager.models import Player, Category, Playlist, Media
from datetime import datetime

from webhook.manager.scripts.update_data import DataManager


def update_or_insert_players(conta, players_from_api):
    """
    Recebe o objeto e inseri a players_from_api no banco de dados. A players_from_api são os players da conta no manager.
    param: conta : Account:
            players_from_api: list of dicts:
    return: records: int: Quantidade de registros inseridos
    """
    # weekDays = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
    num_week = datetime.today().isoweekday()
    records = 0
    i = 0
    while i < len(players_from_api):
        try:
            one_data = players_from_api[i]
            if conta.playlists.filter(playlist_id=one_data['playlists'][str(num_week)]['id']).exists():
                playlist_today = conta.playlists.get(playlist_id=one_data['playlists'][str(num_week)]['id'])
            else:
                account = DataManager(conta.token)
                account.get_playlists()
                update_or_insert_playlists(conta, account.playlists)
                playlist_today = conta.playlists.get(playlist_id=one_data['playlists'][str(num_week)]['id'])

            if conta.players.filter(player_id=one_data['id']).exists():
                Player.objects.filter(player_id=one_data['id']).update(player_id=one_data['id'], name=one_data['name'],
                                                                       platform=one_data['platform'],
                                                                       lastContactInMinutes=one_data['lastContactInMinutes'],
                                                                       group_id=one_data['group']['id'],
                                                                       group_name=one_data['group']['name'],
                                                                       status_id=one_data['playerStatus']['id'],
                                                                       status_name=one_data['playerStatus']['name'],
                                                                       lastLogReceived=one_data['lastLogReceived'],
                                                                       playlist=playlist_today, account=conta)
            else:
                Player.objects.create(player_id=one_data['id'], name=one_data['name'], platform=one_data['platform'],
                                      lastContactInMinutes=one_data['lastContactInMinutes'],
                                      group_id=one_data['group']['id'],
                                      group_name=one_data['group']['name'], status_id=one_data['playerStatus']['id'],
                                      status_name=one_data['playerStatus']['name'],
                                      lastLogReceived=one_data['lastLogReceived'],
                                      playlist=playlist_today, account=conta)
            records += 1
        except Exception as e:
            print('Error: ', e, ' at ', one_data['id'], '-', one_data['name'])
            pass
        i += 1
    return records


def update_or_insert_categories(conta, media_category_from_api):
    records = 0
    i = 0
    while i < len(media_category_from_api):
        try:
            one_data = media_category_from_api[i]
            if conta.categories.filter(category_id=one_data['id']).exists():
                Category.objects.filter(category_id=one_data['id']).update(category_id=one_data['id'],
                                                                           name=one_data['name'],
                                                                           description=one_data['description'],
                                                                           autoShuffle=one_data['autoShuffle'],
                                                                           updateflow=one_data['updateFlow'],
                                                                           account=conta)
            else:
                Category.objects.create(category_id=one_data['id'], name=one_data['name'],
                                        description=one_data['description'],
                                        autoShuffle=one_data['autoShuffle'], updateflow=str(one_data['updateFlow']),
                                        account=conta)
            records += 1
        except Exception as e:
            print('Error: ', e, ' at ', one_data['id'], '-', one_data['name'])
            pass
        i += 1
    return records


def update_or_insert_playlists(conta, playlists_from_api):
    records = 0
    i = 0
    while i < len(playlists_from_api):
        try:
            one_data = playlists_from_api[i]
            if conta.playlists.filter(playlist_id=one_data['id']).exists():
                Playlist.objects.filter(playlist_id=one_data['id']).update(playlist_id=one_data['id'],
                                                                           name=one_data['name'],
                                                                           isSubPlaylist=one_data['isSubPlaylist'],
                                                                           account=conta)
            else:
                Playlist.objects.create(playlist_id=one_data['id'], name=one_data['name'],
                                        isSubPlaylist=one_data['isSubPlaylist'], account=conta)
            records += 1
        except Exception as e:
            print('Error: ', e, ' at ', one_data['id'], '-', one_data['name'])
            pass
        i += 1
    return records


def update_or_insert_medias(conta, medias_from_api):
    records = 0
    i = 0
    while i < len(medias_from_api):
        try:
            one_data = medias_from_api[i]
            categories = category_list_to_objects(conta, one_data['categories'])
            if conta.medias.filter(media_id=one_data['id']).exists():
                Media.objects.filter(media_id=one_data['id']).update(media_id=one_data['id'], name=one_data['name'],
                                                                     file=one_data['file'],
                                                                     durationInSeconds=one_data['durationInSeconds'],
                                                                     startDate=one_data['schedule']['startDate'],
                                                                     endDate=one_data['schedule']['endDate'],
                                                                     # playlist=playlist,
                                                                     account=conta)
                current_media = Media.objects.get(media_id=one_data['id'])
                current_media.category.set(categories)
            else:
                current_media = Media(media_id=one_data['id'], name=one_data['name'], file=one_data['file'],
                                      durationInSeconds=one_data['durationInSeconds'],
                                      startDate=one_data['schedule']['startDate'],
                                      endDate=one_data['schedule']['endDate'],
                                      # playlist=playlist,
                                      account=conta)
                current_media.save()
                for c in categories:
                    current_media.category.add(c)
                current_media.save()
            records += 1
        except Exception as e:
            print('Error: ', e, ' at ', one_data['id'], '-', one_data['name'])
            pass
        i += 1
    return records


def category_list_to_objects(conta, categories_one_media: list):
    """
    Recebe a lista da categorias que possa ter o conteúdo, procura essas categorias no banco e retorna uma lista de objectos
    param: conta : Account:
            categories_one_media: list of dicts: Ex.: [{"id":1, "name":"DEMO"}, {"id":11, "name":"Cliente 1"}]
    return: objects: List of Categories: Lista de Objectos tipo categoria
    """
    i = 0
    list_categories_one_media = list()
    while i < len(categories_one_media):
        one_category = categories_one_media[i]
        if conta.categories.filter(category_id=one_category['id']).exists():
            list_categories_one_media.append(conta.categories.get(category_id=one_category['id']))
        else:
            account = DataManager(conta.token)
            account.get_media_category()
            update_or_insert_categories(conta, account.media_category)
            list_categories_one_media.append(conta.categories.get(category_id=one_category['id']))
        i += 1

    return list_categories_one_media
