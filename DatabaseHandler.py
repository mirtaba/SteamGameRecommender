from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['game_recommender']

bulk_write_val = 100
num_of_datas = 0
datas = []


def insert_user_one(steam_id, games):
    db.users.insert_one({'steam_id': str(steam_id), 'games': games})


def insert_user_bulk(steam_id, games):
    datas.append({'steam_id': str(steam_id), 'games': games})
    global num_of_datas
    num_of_datas += 1
    if num_of_datas >= bulk_write_val:
        exec_inserts()


def exec_inserts():
    if len(datas) > 0:
        db.users.insert_many(datas)
    datas.clear()
    global num_of_datas
    num_of_datas = 0


def is_inserted_before(steam_id):
    res = db.users.find_one({'steam_id': str(steam_id)})
    if res is not None:
        return True
    # looking for duplicate in cache
    for user in datas:
        if user['steam_id'] == steam_id:
            return True

    return False
