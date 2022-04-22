import pygame as py
import json


class JsonManagement:
    def open_file(filename : str) -> dict:
        """ouvre le fichier

        Args:
            filename (str): nom du fichier

        Returns:
            dict: dictionnaire du fichier json
        """
        with open(f'data/{filename}.json', 'r') as f:
            data = json.load(f)
        return data
    
    def write_file(filename : str, data : str) -> None:
        """écrit le fichier

        Args:
            filename (str): nom du fichier
            data (str): données
        """
        with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent = 4, ensure_ascii=False)
            
    def get_specific_information(path : str) -> dict:
        """obtient des infos précises du fichier

        Args:
            path (str): chemin d'acces

        Returns:
            dict: dictionnaire du fichier json
        """
        data = JsonManagement.open_file('saves')
        return eval(f"{data}{path}")
        