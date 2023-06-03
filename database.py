import pymongo
import pymongo.database
import pymongo.collection
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
        return self.get_db()["witanime"]

    def get_anime(self, name: str) -> dict:
        return self.get_anime_collection().find_one({"name": name})
    
    def update_search(self, query: str, data: dict) -> None:
        self.get_anime_collection().update_one({"query": query}, {"$set": data})
    
    def add_anime(self, data: dict) -> None:
        self.get_anime_collection().insert_one(data)
    
    def update_episodes(self, name: str, data: dict) -> None:
        self.get_anime_collection().update_one({"name": name}, {"$set": data})