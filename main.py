import json
from tokenize import Double
from typing import Union

from fastapi import FastAPI,HTTPException
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


class Item(BaseModel):
    username: str
    name: str
    category: str
    image: str
    price: Double
    detail: str



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/games")
def games():
    return json.loads(getOrder())


# @app.get("/games/{item_id}")
# def read_item(item_id: int):
#      with pymongo.MongoClient(cloudDatabase) as conn:
#             db = conn.get_database("LvupShop")
#             where = {'game_id':item_id}
#             cursor = db.Games.find(where)
#             list_cur = list(cursor)
            
#             json_data = dumps(list_cur, ensure_ascii=False)

#             return json_data

@app.get("/games/{name}")
def read_itemname(name: str):
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            where = {'name': {'$regex': name, '$options': 'i'}}
            cursor = db.Games.find(where)
            list_cur = list(cursor)
            if(list_cur==[]):
                raise HTTPException(status_code=404, detail="Item not found")
            json_data = dumps(list_cur, ensure_ascii=False)
            return json_data

@app.get("/login/{email}/{password}")
def read_user(email: str,password: str):
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            where = {"$and":[{'email': email},{'password':password}]}
            cursor = db.Users.find(where)
            list_cur = list(cursor)
            if(list_cur==[]):
                raise HTTPException(status_code=404, detail="User not found")
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
# read_itemname('aaaaa')

@app.get("/order")
def read_order():
      with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            cursor = db.Product.find()
            list_cur = list(cursor)
            
            json_data = dumps(list_cur, ensure_ascii=False)

            return json.loads(json_data)

@app.get("/order/user/{username}")
def read_userOrder(username: str):
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            where = {'username': username}
            cursor = db.Product.find(where)
            list_cur = list(cursor)
            if(list_cur==[]):
                raise HTTPException(status_code=404, detail="Items not found")
            json_data = dumps(list_cur, ensure_ascii=False)
            return json.loads(json_data)


@app.get("/order/{name}")
def read_ordername(name: str):
     with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            where = {'name': {'$regex': name, '$options': 'i'}}
            cursor = db.Product.find(where)
            list_cur = list(cursor)
            if(list_cur==[]):
                raise HTTPException(status_code=404, detail="Item not found")
            json_data = dumps(list_cur, ensure_ascii=False)
            return json.loads(json_data)

@app.post("/order/post")
def post_order(Item: Item):
    with pymongo.MongoClient(cloudDatabase) as conn:
            db = conn.get_database("LvupShop")
            data = {'username':Item.username,'name':Item.name,'category':Item.category,'image':Item.image,'price':Item.price,'detail':Item.detail,'isRecommended': False,'isPopular': False}
            db.Product.insert_one(data)
            return {'status' : 'success','echo':Item}