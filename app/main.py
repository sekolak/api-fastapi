from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from random import randrange
from typing import List
from psycopg2.extras import RealDictCursor
import psycopg2, time
from sqlalchemy.orm import Session
from modules.database import engine
from modules.models import Post
from modules import models, schemas, utils
from collections import defaultdict
from routers import post, user, auth
#import modules.models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  




#while True:

#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', 
#                                cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print ("Database connection was succesfull !!")
#        break
#    except Exception as error:
#        print("Connection to database failed")
#        print("Error; ", error)
#        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "second entrée", "content": "donnes de second entre le sang", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "root route"}
