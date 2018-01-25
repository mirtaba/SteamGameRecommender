from json import JSONDecodeError

import requests
import json
from DatabaseHandler import *


def get_all_games():
    res = requests.get("http://steamspy.com/api.php/", params={'request': 'all'})
    try:
        games = json.loads(res.content.decode('utf-8'))
    except JSONDecodeError:
        return 1

    return games


def insert_games_to_db(games):
    games_list = []
    for appid, game in games.items():
        games_list.append(game)

    insert_games_bulk(games_list)

if __name__ == '__main__':
    insert_games_to_db(get_all_games())
# get_all_games()