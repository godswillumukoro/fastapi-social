from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body # used for handling request bodies in API endpoints
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor # give column names from DB
import time
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




while True:
    try:
        db_connection = psycopg2.connect(
            host='localhost',
            database='fastapi-social',
            user='postgres',
            password='postgres'
        )
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        print("DB Connection Successful")
        break
    except Exception as error:
        print("DB Connection Failed")
        print("Error: ", error)
        time.sleep(2)

def find_post(post_id):
    for post in postsStore:
        if post["id"] == post_id:
            return post

def find_post_index(post_id):
    for i, post in enumerate(postsStore):
        if post["id"] == post_id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts/latest")
def get_latest_post():
    try:
        cursor.execute(""" SELECT * FROM posts ORDER BY posts.id DESC LIMIT 2 """)
        latest_posts = cursor.fetchall()

        if not latest_posts:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

        return {"data": latest_posts}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)): # path operator function
    try:
        # cursor.execute(""" SELECT * FROM posts WHERE id= %s """, (id,))
        # post = cursor.fetchone()
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} not found")
        #     response.status_code = status.HTTP_404_NOT_FOUND
        #     return{"message": f"post: {id} not found"}
        return {"data": post}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.is_published))

    # db_connection.commit() # push changes to DB

    # new_post = cursor.fetchone()

    new_post = models.Post(**post.dict())
    # new_post = models.Post(title = post.title, content = post.content, is_published = post.is_published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        # cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING * """, (id,))
        # db_connection.commit()

        # del_post = cursor.fetchone()

        del_post = db.query(models.Post).filter(models.Post.id == id)

        if not del_post.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} not found")

        del_post.delete(synchronize_session = False)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        # cursor.execute(""" UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING * """,
        #                 (post.title, post.content, post.is_published, (id,)))
        # db_connection.commit()

        # updated_post = cursor.fetchone()

        updated_post = db.query(models.Post).filter(models.Post.id == id)

        if not updated_post.first():
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} not found")

        updated_post.update(post.dict(), synchronize_session = False)
        db.commit()
        return {"data": updated_post.first()}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))