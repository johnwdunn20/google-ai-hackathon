# check for new keys
def check_for_new_keys(json1, json2):
    new_keys = []
    for key in json1.keys():
        if key not in json2.keys():
            new_keys.append(key)
    return new_keys