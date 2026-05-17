from pydantic import BaseModel


class Create(BaseModel):
    name : str
    email : str
    password : str

class ShowUser(BaseModel):
    id : int
    name : str
    email : str

class user_data(BaseModel):
    name : str
    email : str
    password : str