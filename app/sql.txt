import time
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# PostgreSQL Connection
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="admin",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)
        time.sleep(2)

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    rating: Optional[int] = None

    class Config:
        from_attributes = True

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate):
    cursor.execute(
        "INSERT INTO post (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *",
        (post.title, post.content, post.published, post.rating)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM post WHERE id = %s RETURNING id", (id,))
    deleted = cursor.fetchone()
    conn.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

@app.put("/posts/{id}")
def update_post(id: int, post: PostCreate):
    cursor.execute(
        "UPDATE post SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, post.rating, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": updated_post}

