import json

def get_form_data():
    try:
        with open('form_data.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    return data

from my_module import get_form_data

data = get_form_data()
print(data)

