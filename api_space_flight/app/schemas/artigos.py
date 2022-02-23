from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional




class Evento(BaseModel):
    id :int
    provider :str
    class Config:
        orm_mode = True
   
class Launch(BaseModel):
    id :str
    provider :str
    class Config:
        orm_mode = True

class Artigo(BaseModel):
    id:int
    featured:bool
    title :str
    url:str 
    image_url:str 
    news_site:str
    summary:str
    publishiedAt:datetime
    
    events :List[Evento]= []
    launchers :List[Launch]= []

    class Config:
        orm_mode = True


