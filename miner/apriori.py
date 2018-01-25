from itertools import combinations, chain

from DatabaseHandler import *

min_support = db.users.count() * 0.001
min_confidence = db.users.count() * 0.01


def run():
    large_set = {}
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assoc_rules = {}
    # Dictionary which stores Association Rules

    C1 = []
    for game in db.games.find():
        C1.append(frozenset([game.get('appid')]))

    currentL = get_items_satisfying_minsupp(C1)

    k = 2
    while currentL != set([]):
        large_set[k - 1] = currentL
        currentL = get_items_satisfying_minsupp(join_set(currentL, k))
        k = k + 1

    to_ret_items = []
    for key, value in large_set.items():
        for item in value:
            to_ret_items.append((tuple(item), cal_support(item)))

    to_ret_rules = []
    # for key, value in large_set.items()[1:]:
    #     for item in value:
    #         _subsets = map(frozenset, [x for x in subsets(item)])
    #         for element in _subsets:
    #             remain = item.difference(element)
    #             if len(remain) > 0:
    #                 confidence = cal_support(item) / cal_support(element)
    #                 if confidence >= min_confidence:
    #                     to_ret_rules.append(((tuple(element), tuple(remain)), confidence))

    return to_ret_items, to_ret_items


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def join_set(l_set, size):
    new_c_set = set()
    for i in l_set:
        for j in l_set:
            uni = i.union(j)
            if len(uni) == size:
                new_c_set.add(uni)

    return new_c_set


def get_items_satisfying_minsupp(c_set):
    res_set = set()
    for item_set in c_set:
        supp = cal_support(item_set)
        print(str(item_set) + " ---> supp: " + str(supp))
        if min_support <= supp:
            res_set.add(item_set)

    return res_set


def cal_support(item_set):
    supp = db.users.find({'games': {'$all': list(item_set)}}).count()
    # db.assoc_rules.insert_one({'item_set': list(item_set), 'support': supp})
    return supp


def printResults(items):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    # for rule, confidence in sorted(rules, key=lambda x: x[1]):
    #     pre, post = rule
    #     print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


if __name__ == '__main__':
    # item_sets, rules = run()
    # printResults(item_sets)
    input("please enter steam id:")

    print("recommended games for you:")
    game = db.games.find({'appid': 304930})[0]
    print("name         positive percent")
    print(str(game['name']) + "    " + str(game['positive']*100 / (game['positive'] + game['negative'])))

    print("Confidence: ")
    print(cal_support({578080, 730, 304930}) / cal_support({578080, 730}))
    print("Lift: ")
    print(cal_support({578080, 730, 304930}) * db.users.find().count() / (
            cal_support({578080, 730}) * cal_support({304930})))

    # import data_fetcher.get_users as dd
    #
    # cnt, g = dd.get_owned_games(76561198023653599)
    # print(g)
