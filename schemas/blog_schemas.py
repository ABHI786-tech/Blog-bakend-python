from pydantic import BaseModel

from schemas.users_schema import ShowUser


class Blog(BaseModel):
    title: str
    body: str
    


class showBlog(Blog):
    creator: ShowUser
    


    class Config:
        from_attributes = True
        
        