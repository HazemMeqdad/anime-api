import pymongo
import pymongo.database
import typing as t



class Database:
    def __init__(self, db_url: str) -> None:
        self.url = db_url

    def connect(self) -> pymongo.MongoClient:
        self.client = pymongo.MongoClient(self.url)
        return self.client
    
    def get_db(self) -> pymongo.database.Database:
        return self.client["anime"]

    def get_anime_collection(self) -> pymongo.collection.Collection:
        return self.get_db()["winanime"]

    def get_anime(self, name: str) -> dict:
        return self.get_anime_collection().find_one({"name": name})
    