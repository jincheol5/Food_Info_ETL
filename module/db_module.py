from datetime import datetime,timezone
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class MongoDBInterface:
    def __init__(self,port:int=27017):
        self.port=port
        self.connect_db()

    def connect_db(self):
        try:
            self.client=MongoClient(f"mongodb://127.0.0.1:{self.port}/")
            self.db=self.client["chronolab"]
            self.nutrition=self.db["nutrition"] # nutrition info collection
        except PyMongoError as e:
            print(f"MongoDB error: {e}")

    def disconnect_db(self):
        self.client.close()

    def delete_collection(self,collection_name:str):
        if self.client is None:
            self.connect_db()
        collection=self.db[collection_name]
        try:
            collection.delete_many({})
            print(f"{collection_name} collection is deleted!")
        except PyMongoError as e:
            print(f"MongoDB error: {e}")

    def insert_food(self,food_ids:list):
        """
        Insert foods to DB
        """
        food_info_map={
            food_id:{
                "_id":food_id,
                "food_id":food_id,
                "extracted":False,
                "validated":False,
                "created_t":datetime.now(timezone.utc), # BSON의 Date 타입 (ISODate)으로 저장
                "extracted_t":None, # update 시 datetime.now(timezone.utc)
                "validated_t":None, # update 시 datetime.now(timezone.utc)
                "nutrition":None
            }
            for food_id in food_ids
        }
        food_info_list=list(food_info_map.values())
        try:
            self.nutrition.insert_many(food_info_list,ordered=False) # ordered=False: 중복 _id 있으면 skip
        except PyMongoError as e:
            print(f"MongoDB error: {e}")

    def get_unextracted_food(self):
        """
        영양성분 정보가 추출되지 않은 food id list 반환
        """
        try:
            food_ids=list(
                doc["_id"]
                for doc in self.nutrition.find(
                    {"extracted":False,"validated":False}, # 조건 (filter)
                    {"_id":1} # 가져올 필드 (projection)
                )
            )
            return food_ids
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
            return []

    def update_nutrition_info(self,nutrition_info_list:list):
        for nutrition_info in nutrition_info_list:
            """
            nutrition_info
                (food_id,result)
            """
            food_id=nutrition_info[0]
            result=nutrition_info[1]
            try:
                self.nutrition.update_one(
                    {"_id":food_id},
                    {
                        "$set":{
                            "extracted":True,
                            "extracted_t":datetime.now(timezone.utc),
                            "nutrition":result
                        }
                    }
                )
            except PyMongoError as e:
                print(f"MongoDB error: {e}")
                continue