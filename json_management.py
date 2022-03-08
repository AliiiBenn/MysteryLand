import pygame as py
import json


class JsonManagement:
    def open_file(filename : str) -> dict:
        '''
        ouvre le fichier
        '''
        with open(f'data/{filename}.json', 'r') as f:
            data = json.load(f)
        return data
    
    def write_file(filename : str, data : str) -> None:
        '''
        écrit le fichier
        '''
        with open(f'data/{filename}.json', 'w') as f:
            json.dump(data, f, indent = 4)
            
    def get_specific_information(path : str) -> dict:
        '''
        obtient des infos précises du fichier
        '''
        data = JsonManagement.open_file('saves')
        return eval(f"{data}{path}")
        