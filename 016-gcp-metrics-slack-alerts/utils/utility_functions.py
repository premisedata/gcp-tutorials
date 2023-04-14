def merge_lists(list_1, list_2):
    for dict1 in list_1:
        for dict2 in list_2:
            if dict1['name'] == dict2['name']:
                dict1.update(dict2)
    return list_1