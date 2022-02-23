
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,Date,ForeignKey,ARRAY
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import TSVectorType
from sqlalchemy import select
from sqlalchemy.sql.functions import count
from sqlalchemy import func,and_


Base = declarative_base()


class Artigo(Base):
    __tablename__= "dbartigos"
    
    id = Column(Integer,autoincrement=True,primary_key=True,unique=True,name="id")
    featured_input = Column(Integer,name="featured")
    #-----------------------------------------------------
    title =  Column(String,name="title")
    url =  Column(String,name="url")
    image_url =  Column(String,name="image_url")
    news_site =  Column(String,name="news_site")
    summary =  Column(String,name="summary")
    publishiedAt =  Column(Date,name="publishiedat")
    deletado  =  Column(Date,name="dtend")
    
    events = relationship("Event",uselist=True,back_populates="artigo",primaryjoin="and_(Event.id_artigo == Artigo.id,Event.deletado == None)")
    launchers = relationship("Launch",back_populates="artigo",uselist=True,primaryjoin="and_(Launch.id_artigo == Artigo.id,Launch.deletado == None)")

    @hybrid_property
    def featured(self):
        if self.featured_input:
            return True
        return False

class Event(Base):
    __tablename__= "artigos_events"
    
    id = Column(Integer,primary_key=True,unique=True,name="id")
    id_artigo = Column(Integer,ForeignKey(Artigo.id),name="id_artigo")
    provider = Column(String,name="provider")
    deletado  =  Column(Date,name="dtend")
    
    artigo = relationship("Artigo",uselist=False,back_populates="events")



class Launch(Base):
    __tablename__= "artigos_lauchers"
    
    id = Column(Integer,primary_key=True,unique=True,name="id")
    id_artigo = Column(Integer,ForeignKey(Artigo.id),name="id_artigo")
    provider = Column(String,name="provider")
    deletado  =  Column(Date,name="dtend")
    
    artigo = relationship("Artigo",uselist=False,back_populates="launchers")

