import json
from typing import Union

from fastapi import FastAPI
import pymongo
import dns
from bson.json_util import dumps
from pydantic import BaseModel

cloudDatabase = 'mongodb+srv://admin:1913210736@cluster0.jig4l.mongodb.net/myFirstDatabase?ssl=true&ssl_cert_reqs=CERT_NONE'

app = FastAPI()

class User(BaseModel):
    profileImage: str
    email: str
    password: str
    username: str
    birth: str
    gender: str



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/games")
def games():
    return json.loads(getOrder())


@app.get("/games/{item_id}")
def read_item(item_id: int):
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            where = {'game_id':item_id}
            cursor = db.Games.find(where)
            list_cur = list(cursor)
            
            json_data = dumps(list_cur, ensure_ascii=False)

            return json_data

@app.get("/games/name/{name}")
def read_itemname(name: str):
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            where = {'name': {'$regex': name, '$options': 'i'}}
            cursor = db.Games.find(where)
            list_cur = list(cursor)
            json_data = dumps(list_cur, ensure_ascii=False)
            return json_data

@app.get("/login/{email}/{password}")
def read_user(email: str,password: str):
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            where = {"$and":[{'email': email},{'password':password}]}
            cursor = db.Users.find(where)
            list_cur = list(cursor)
            json_data = dumps(list_cur, ensure_ascii=False)
            return json.loads(json_data)

@app.post("/regis")
def regis_user(user: User):
    with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            data = {'username':user.username,'email':user.email,'password':user.password,'gender':user.gender,'birthday':user.birth,'description':'','guarantee': False,'star':0,'profileImage':user.profileImage}
            db.Users.insert_one(data)
            return {'status' : 'success','echo':user}
    

def getOrder():
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            cursor = db.Games.find()
            list_cur = list(cursor)
            
            json_data = dumps(list_cur, ensure_ascii=False)

            return json_data

# print(json.loads(getOrder()))
