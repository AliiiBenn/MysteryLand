import firebase_admin
from firebase_admin import credentials, db


class DatabaseLink:
    def __init__(self):
        self.cred = credentials.Certificate("data/serviceAccountKey.json")
        self.initialize_app()
        self.ref = db.reference('database/')
        self.users_ref = self.create_child('users')
        
    def initialize_app(self):
        """initialise l'app de la base de donnée 

        Returns:
            _type_: base de donnée
        """
        return firebase_admin.initialize_app(self.cred, {'databaseURL' : 'https://mysteryland-fb22d-default-rtdb.europe-west1.firebasedatabase.app/'})
    
    def create_child(self, child_name : str):
        """créer un child

        Args:
            child_name (str): nom

        Returns:
            _type_: child de nom child_name
        """
        return self.ref.child(child_name)
    
    