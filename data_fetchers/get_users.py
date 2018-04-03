from json import JSONDecodeError

import requests
import json
from handlers.DatabaseHandler import *

steamKeyFile = open('apiKey.key', 'r')
steam_api_key = steamKeyFile.read(45)


def get_friend_list(steam_id):
    try:
        res = requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/",
                           params={'key': steam_api_key, 'steamid': steam_id, 'relationship': 'all'})
    except ConnectionError:
        return None

    try:
        friends = json.loads(res.content.decode('utf-8')).get('friendslist').get('friends')
    except:
        return None

    # friends in form of array -->
    # [{'steamid': '76561197960265731', 'relationship': 'friend', 'friend_since': 0}, ...]
    return friends


def get_owned_games(steam_id):
    try:
        res = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/",
                           params={'key': steam_api_key, 'steamid': steam_id})
    except ConnectionError:
        return 0, None
    try:
        game_dict = json.loads(res.content.decode('utf-8')).get('response')
    except:
        return 0, None
    game_count = game_dict.get('game_count')
    games = game_dict.get('games')

    # games is form of array --> [{'appid': 201810, 'playtime_forever': 387}, ...]
    return game_count, games


def get_new_steam_id(steam_id):
    return str(int(steam_id) - 76561197960265728)


def get_wishlist(steam_id):
    new_steam_id = get_new_steam_id(steam_id)
    res = requests.get("http://store.steampowered.com/dynamicstore/userdata/",
                       params={"id": new_steam_id})
    try:
        wishlist = json.loads(res.content.decode('utf-8')).get('rgWishlist')
    except JSONDecodeError:
        return []

    # friends in form of array -->
    # [{'steamid': '76561197960265731', 'relationship': 'friend', 'friend_since': 0}, ...]
    return wishlist


def insert_user_to_db(steam_id):
    # This avoidance is not relevant in the new method
    # Avoid duplicate inserts
    # if is_inserted_before(steam_id):
    #    return 0

    total_games, games = get_owned_games(steam_id)
    friends = get_friend_list(steam_id)
    # wishlist = get_wishlist(steam_id)
    # for Private accounts
    if games is None:
        return 0
    if friends is None:
        return 0

    return insert_user_buffer(steam_id, total_games, games, friends, [])




# TODO: add each user wishlist to the info


def run():
    count = 0
    seed_steam_id = last_added_user()
    steam_id = str(int(seed_steam_id) + 1)
    try:
        while True:
            is_added = insert_user_to_db(steam_id)
            steam_id = str(int(steam_id) + 1)
            if is_added == 1:
                print(steam_id)
            count = count + is_added
            if count == 10:
                flush_users()
                count = 0
    except:
        flush_users()
    print('something went wrong and program stopped')


if __name__ == '__main__':
    while True:
        run()
