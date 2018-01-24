from json import JSONDecodeError

import requests
import json
from datetime import datetime, timedelta
from DatabaseHandler import *

steam_api_key = '532BCE1457C92CBA3F93BB5BBAF84A16'
game_time_played_threshold = 100
seed_steam_ids = ['76561198023653599']
seed_max_size = 100 * 100 * 100


def get_player_summaries(steam_ids):
    ids_string = str(steam_ids).replace("'", "").replace('[', '').replace(']', '').replace(' ', '')

    res = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/",
                       params={'key': steam_api_key, 'steamids': ids_string})

    print(res.content.decode('utf-8'))

    # TODO: complete this function if you wanna use


def get_friend_list(steam_id):
    res = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/",
                       params={'key': steam_api_key, 'steamid': steam_id, 'relationship': 'all'})
    try:
        friends = json.loads(res.content.decode('utf-8')).get('friendslist').get('friends')
    except JSONDecodeError:
        return []

    # friends in form of array -->
    # [{'steamid': '76561197960265731', 'relationship': 'friend', 'friend_since': 0}, ...]
    return friends


def get_owned_games(steam_id):
    try:
        res = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/",
                           params={'key': steam_api_key, 'steamid': steam_id})
    except ConnectionError:
        return 0, None
    game_dict = json.loads(res.content.decode('utf-8')).get('response')

    game_count = game_dict.get('game_count')
    games = game_dict.get('games')

    # games is form of array --> [{'appid': 201810, 'playtime_forever': 387}, ...]
    return game_count, games


def insert_user_to_db(steam_id):
    # Avoid duplicate inserts
    if is_inserted_before(steam_id):
        return 0

    total_games, games = get_owned_games(steam_id)

    # for Private accounts
    if games is None:
        return 1

    game_ids = []

    for game in games:
        if game['playtime_forever'] >= game_time_played_threshold:
            game_ids.append(game['appid'])

    if len(game_ids) > 0:
        # User one of below:
        insert_user_bulk(steam_id, game_ids)
        # insert_user_one(steam_id, game_ids)

    return 0


def run(time_until):
    while len(seed_steam_ids) > 0:
        if datetime.now() > time_until:
            print('time finished')
            break

        steam_id = seed_steam_ids.pop()
        is_private = insert_user_to_db(steam_id)

        if is_private == 0:
            for friend in get_friend_list(steam_id):
                friend_steam_id = friend['steamid']
                # print(str(friend_steam_id))
                if not is_inserted_before(friend_steam_id) and len(seed_steam_ids) < seed_max_size:
                    seed_steam_ids.append(friend_steam_id)
    exec_inserts()


if __name__ == '__main__':
    run(datetime.now() + timedelta(minutes=1))
