import pygame as py
import json


class JsonManagement:
    def open_file(filename):
        with open(f'data/{filename}.json', 'r') as f:
            data = json.load(f)
        return data
    
    def write_file(filename, data):
        with open(f'data/{filename}.json', 'w') as f:
            json.dump(data, f, indent = 4)
            
    def get_specific_information(path):
        data = JsonManagement.open_file('saves')
        return eval(f"{data}{path}")
        