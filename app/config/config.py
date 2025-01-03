import json

def load_clients(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)
