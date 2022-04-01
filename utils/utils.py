import json

def float_to_string(flt: float):
    return str(flt).split('.')[0]

def get_keys_of_dict(dict: dict):
    keys = []
    for key in dict:
        keys.append(key)
    return keys

def double_quote_dict(dict: str):
    return dict.replace("'", '"')
