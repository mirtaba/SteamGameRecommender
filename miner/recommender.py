from DatabaseHandler import db
from miner.apriori import cal_support
from data_fetcher.get_users import get_owned_games
import itertools
import pymongo

playtime_threshold = 720
confidence_threshold = 0.01
lift_threshold = 1


def cal_confidence(item_set, goal_set):
    return cal_support(item_set + goal_set) / cal_support(item_set)


def cal_lift(item_set, goal_set):
    return cal_support(item_set + goal_set) / (cal_support(item_set) * cal_support(goal_set))


def including_sets_sort_by_support(item_set):
    return db.games_set.find({'item_set': {'$all': item_set}}).sort([('support', pymongo.DESCENDING)])


def user_recommended_games(steam_id):
    count, user_games = get_owned_games(steam_id)
    print(count)
    too_low_games = []
    for game in user_games:
        if game.get('playtime_forever') < playtime_threshold:
            too_low_games.append(game)
    for game in too_low_games:
        user_games.remove(game)
    print(len(user_games))

    recommending_games = [];
    for i in range(len(user_games), 0, -1):
        comb_list = list(itertools.combinations(user_games, i))
        for item_list in comb_list:
            tmp = []
            for item in item_list:
                tmp.append(item['appid'])
            item_list = tmp
            # print(item_list)
            if len(item_list) == 1 and item_list[0] == 730:
                print(item_list)

            supporting_sets = including_sets_sort_by_support(item_list)
            supporting_sets = list(supporting_sets)

            if len(item_list) == 1 and item_list[0] == 730:
                print(supporting_sets)

            for sup_set in supporting_sets:

                rest_of_set = [x for x in sup_set if x not in item_list]
                confidence = cal_confidence(item_list, rest_of_set)
                lift = cal_lift(item_list, rest_of_set)
                if confidence > confidence_threshold and lift > lift_threshold:
                    for good_game in rest_of_set:
                        recommending_games.append(good_game["appid"])

    return recommending_games;

if __name__ == '__main__':
    print(user_recommended_games("76561198023653599"))


