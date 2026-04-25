from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"id": 1, "title": "title of post 1", "content": "content of post 1", "published": True, "rating": 5}]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
@app.post("/createposts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}
@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"post_detail": post}
    return {"message": f"post with id: {id} was not found"}

