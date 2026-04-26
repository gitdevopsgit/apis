from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ============ PostgreSQL Connection (COMMENTED OUT) ============
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="admin",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Database connection failed!")
#         print("Error:", error)
#         time.sleep(2)

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

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

# ============ GET /posts - Using SQLAlchemy ============
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

# ============ Previous PostgreSQL version (COMMENTED OUT) ============
# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM post")
#     posts = cursor.fetchall()
#     return {"data": posts}

# ============ POST /createposts - Using SQLAlchemy ============
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published,
        rating=post.rating
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# ============ Previous PostgreSQL version (COMMENTED OUT) ============
# @app.post("/createposts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: PostCreate):
#     cursor.execute(
#         "INSERT INTO post (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *",
#         (post.title, post.content, post.published, post.rating)
#     )
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}

# ============ GET /posts/{id} - Using SQLAlchemy ============
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# ============ Previous PostgreSQL version (COMMENTED OUT) ============
# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return {"post_detail": post}

# ============ DELETE /posts/{id} - Using SQLAlchemy ============
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    db.delete(post)
    db.commit()

# ============ Previous PostgreSQL version (COMMENTED OUT) ============
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("DELETE FROM post WHERE id = %s RETURNING id", (id,))
#     deleted = cursor.fetchone()
#     conn.commit()
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

# ============ PUT /posts/{id} - Using SQLAlchemy ============
@app.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    db_post.rating = post.rating

    db.commit()
    db.refresh(db_post)
    return {"data": db_post}

# ============ Previous PostgreSQL version (COMMENTED OUT) ============
# @app.put("/posts/{id}")
# def update_post(id: int, post: PostCreate):
#     cursor.execute(
#         "UPDATE post SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
#         (post.title, post.content, post.published, post.rating, id)
#     )
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return {"data": updated_post}

# ============ GET /users - Using SQLAlchemy ============
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"data": users}

# ============ POST /users - Create User Using SQLAlchemy ============
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": new_user}

# ============ GET /users/{id} - Using SQLAlchemy ============
@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return {"user_detail": user}

# ============ DELETE /users/{id} - Using SQLAlchemy ============
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    db.delete(user)
    db.commit()

# ============ PUT /users/{id} - Using SQLAlchemy ============
@app.put("/users/{id}")
def update_user(id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name

    db.commit()
    db.refresh(db_user)
    return {"data": db_user}
