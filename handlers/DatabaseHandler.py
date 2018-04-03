from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['NewSteamUsers']

bulk_write_val = 100

datas = []


def insert_user_one(steam_id, total_games, games, friends, wishlist):
    db.users.insert_one({'steam_id': str(steam_id), 'game_count': total_games, 'games': games,
                         'friends': friends, 'wishlist': wishlist})


def insert_user_buffer(steam_id, total_games, games, friends, wishlist):
    if not(is_inserted_before(steam_id)):
        datas.append({'steam_id': str(steam_id), 'game_count': total_games, 'games': games,
                     'friends': friends, 'wishlist': wishlist})
        return 1
    else:
        return 0


def flush_users():
    print(datas)
    if len(datas) > 0:
        db.users.insert_many(datas)
    datas.clear()


def insert_games_bulk(games):
    db.games.insert_many(games)


def is_inserted_before(steam_id):
    res = db.users.find_one({'steam_id': str(steam_id)})
    if res is not None:
        return True
    # looking for duplicate in cache
    for user in datas:
        if user['steam_id'] == steam_id:
            return True

    return False


def last_added_user():
    res = db.users.find().sort([('steam_id', -1)]).limit(1)
    return res.next()['steam_id']

def get_inline_iterator():
    res = db.users.find().sort([('steam_id', 1)])
    return res


if __name__ == '__main__':
    last_added_user()
    db.users.insert_many([{"chert": "test"}, {"chert": "test2"}])
