import json


FILENAME = 'settings.json'


def save(data, filename=FILENAME):
    """Saves info to file"""
    with open(filename, 'w', encoding='UTF-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load(filename=FILENAME):
    """Loads info from file"""
    try:
        with open(filename, encoding='UTF-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {
            'best_score': 0,
            'settings': {
                'hardness': 1,
                'control_type': 'm',
                'language': 'EN'
            }
        }
        save(data)

    return data
