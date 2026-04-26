from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# In-memory database
my_posts = [{"id": 1, "title": "title of post 1", "content": "content of post 1", "published": True, "rating": 5}]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for index, p in enumerate(my_posts):
        if p["id"] == id:
            my_posts[index] = post.model_dump()
            my_posts[index]["id"] = id
            return {"data": my_posts[index]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

