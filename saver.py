import json


FILENAME = 'settings.json'


def load(filename=FILENAME):
    """Loads info from file"""
    with open(filename, encoding='UTF-8') as file:
        data = json.load(file)

    return data
