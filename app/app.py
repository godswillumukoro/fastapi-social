from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body # used for handling request bodies in API endpoints
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor # give column names from DB
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user


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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}
