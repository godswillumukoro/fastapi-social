from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix = '/posts'
)

@router.get('/', response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.get("/latest", response_model=List[schemas.PostResponse])
def get_latest_post():
    try:
        cursor.execute(""" SELECT * FROM posts ORDER BY posts.id DESC LIMIT 2 """)
        latest_posts = cursor.fetchall()

        if not latest_posts:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

        return latest_posts

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)): # path operator function
    try:
        # cursor.execute(""" SELECT * FROM posts WHERE id= %s """, (id,))
        # post = cursor.fetchone()
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} not found")
        #     response.status_code = status.HTTP_404_NOT_FOUND
        #     return{"message": f"post: {id} not found"}
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.is_published))

    # db_connection.commit() # push changes to DB

    # new_post = cursor.fetchone()

    new_post = models.Post(**post.dict())
    # new_post = models.Post(title = post.title, content = post.content, is_published = post.is_published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schemas.PostResponse)
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
        return updated_post.first()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
