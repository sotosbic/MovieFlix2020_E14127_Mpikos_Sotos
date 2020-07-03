import os
from pymongo import MongoClient
from pprint import pprint

# Class that simplifies the Mongo Connection init and close and some extra methods
class Mongo():
    def __init__(self):    
        
        self.client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
        self.db = self.client.MovieFlix

    def auth_check(self, mail, pwd):
        if self.db.Users.count_documents({"e-mail": mail, "password": pwd }, limit = 1):
            return True

    def getCategoty(self, mail):
        print(self.db.Users.find({"e-mail": mail }, {"category":1, "_id":0},limit=1)[0]['category'])
        return self.db.Users.find({"e-mail": mail }, {"category":1, "_id":0},limit=1)[0]['category']

    def getID(self, mail):
        return self.db.Users.find_one({"e-mail": mail }).get('_id')

    def close(self):
        self.client.close()


