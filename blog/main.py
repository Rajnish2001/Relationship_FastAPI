from typing import List
from fastapi import FastAPI,Depends,HTTPException,status
from .database import get_db,SessionLocal,Base,engine
from .import models
from .schemas import Blog,User,ShowUser,ShowBlog
# from passlib.context import CryptContext
from .hashing import Hash


app = FastAPI(title="Routers in FastAPI")

#Creating all database table
models.Base.metadata.create_all(bind=engine)

@app.post('/blog',tags=['Blogs'])
def blog(request:Blog,db:SessionLocal=Depends(get_db)):
    blog_data = models.Blog(title=request.title,blog=request.blog,creator_id=request.creator_id)
    db.add(blog_data)
    db.commit()
    db.refresh(blog_data)
    return blog_data

@app.get('/blog',tags=['Blogs'],response_model=List[ShowBlog])
def all_blog(db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog

@app.get('/blog/{id}',tags=['Blogs'],response_model=ShowBlog)
def all_blog(id,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Blog id {id} is Not Found!')
    return blog

@app.delete('/blog/{id}',tags=['Blogs'])
def delete_blog(id,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Blog id {id} is Not Found!')
    db.delete(blog)
    db.commit()
    return 'Blog is deleted'



# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/user',tags=['Users'],response_model=ShowUser)
def blog(request:User,db:SessionLocal=Depends(get_db)):
    # hash_password = pwd_context.hash(request.password)
    user = models.User(name=request.name,email=request.email,password=Hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/user',tags=['Users'],response_model=List[ShowUser])
def all_blog(db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).all()
    return user

@app.get('/user/{id}',tags=['Users'],response_model=ShowUser)
def all_blog(id,db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'User id {id} is Not Found!')
    return user

@app.delete('/user/{id}',tags=['Users'])
def delete_blog(id,db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'User id {id} is Not Found!')
    db.delete(user)
    db.commit()
    return 'User is deleted'