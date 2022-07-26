from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title : str
    blog : str
    creator_id :int

class User(BaseModel):
    name : str
    email : str
    password : str

class UserBlog(BaseModel):
    title : str
    blog : str
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    name : str
    email : str
    blogs : List[UserBlog] = []
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title : str
    blog : str
    creator : ShowUser

    class Config():
        orm_mode = True