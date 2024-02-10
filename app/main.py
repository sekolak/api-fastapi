from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
from typing import List
from psycopg2.extras import RealDictCursor
import psycopg2, time
from sqlalchemy.orm import Session
from modules.database import engine, get_db
from modules.models import Post
from modules import models, schemas, utils
from collections import defaultdict
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
        
@app.get("/")
def root():
    return {"message": "Assalamu Alaykum ya ikhwan"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
#    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
#                   (post.title, post.content, post.published))
#    new_post = cursor.fetchone()
#    conn.commit()
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #new_post = models.Post(**jsonable_encoder(post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
#    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
#    post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

#    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
#    deleted_post= cursor.fetchone()
#    conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

#    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#                    (post.title, post.content, post.published, (str(id))))

#    updated_post = cursor.fetchone()
#    conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}


#Creation de users, 5H55 
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #first create the hash of the password
    hashed_password = utils .hash(user.password)
    user.password = hashed_password

    #new_post = models.User(**vars(user))
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
   user =  db.query(models.User).filter(models.User.id == id).first()

   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"User with id: {id} does not exist")
   return user