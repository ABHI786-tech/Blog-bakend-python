from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from config.token import get_current_user
from cors.database import get_db
from models import blog_model
from schemas.blog_schemas import Blog, showBlog
from schemas.users_schema import user_data

blog_route = APIRouter(prefix="/blog", tags=["Blog"])


#  view all blog
@blog_route.get("/", response_model=List[showBlog])
def allBlogs(
    db: Session = Depends(get_db), current_user: user_data = Depends(get_current_user)
):
    blogs = db.query(blog_model.Blog).all()
    return blogs


# create a blog
@blog_route.post("/create", status_code=status.HTTP_201_CREATED)
def create_blog(
    request: Blog,
    db: Session = Depends(get_db),
    current_user: user_data = Depends(get_current_user),
):
    new_blog = blog_model.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# view single blog
@blog_route.get("/{id}", status_code=200, response_model=Blog)
def viewBlog(
    id,
    db: Session = Depends(get_db),
    current_user: user_data = Depends(get_current_user),
):
    singleBlog = db.query(blog_model.Blog).filter(blog_model.Blog.id == id).first()
    if not singleBlog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the bog id {id} in not available",
        )
    return singleBlog


# delete blog
@blog_route.delete("/{id}", status_code=status.HTTP_200_OK)
def deleteBlog(
    id,
    db: Session = Depends(get_db),
    current_user: user_data = Depends(get_current_user),
):
    blog = db.query(blog_model.Blog).filter(blog_model.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the blog with id {id} is not available",
        )

    blog.delete(synchronize_session=False)
    db.commit()

    return {"detail": "Blog deleted successfully"}


#  update blog
@blog_route.put("/{id}")
def updateBlog(
    id,
    request: Blog,
    db: Session = Depends(get_db),
    current_user: user_data = Depends(get_current_user),
):
    blog = db.query(blog_model.Blog).filter(blog_model.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the blog with id {id} is not available",
        )

    blog.update(request.model_dump())
    db.commit()
    return "updated successfully"
