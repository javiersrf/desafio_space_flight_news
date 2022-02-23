import datetime
from fastapi.exceptions import HTTPException
from starlette import  status
from sqlalchemy.orm import Session
from random import randint
from sqlalchemy import or_
from schemas import artigos
from modelos.artigo import Artigo,Event,Launch

def get_todos_artigos(db:Session,pagina:int = 1):
    artigos = db.query(
        Artigo
        ).filter(
           Artigo.deletado==None
            ).order_by(
                Artigo.id.asc()
                ).offset((pagina-1)*20).limit(20).all()
    
    return artigos


def get_artigo_pelo_id(id:int,db:Session):
    artigo = db.query(
        Artigo
        ).filter(
           Artigo.deletado==None,Artigo.id == id
            ).first()
    if artigo ==None:
        raise HTTPException(
            status_code=204,
            detail="Artigo não encontrado"
        )
    return artigo
def insert_novo_artigo(db:Session,artigo_input:artigos.Artigo):
    novo_artigo = Artigo()
    novo_artigo.id = artigo_input.id
    if artigo_input.featured:
        novo_artigo.featured_input = 1
    else:
        novo_artigo.featured_input = 0
    novo_artigo.title = artigo_input.title
    novo_artigo.url = artigo_input.url 
    novo_artigo.image_url = artigo_input.image_url 
    novo_artigo.news_site = artigo_input.news_site
    novo_artigo.summary = artigo_input.summary
    novo_artigo.publishiedAt = artigo_input.publishiedAt
    db.add(novo_artigo)
    try:
        db.add_all([Event(id = x.id, id_artigo = artigo_input.id,  provider = x.provider,) for x in artigo_input.events])
        db.add_all([Launch(id = x.id, id_artigo = artigo_input.id,  provider = x.provider,) for x in artigo_input.events])
        db.commit()
    except:
       raise HTTPException(
            status_code=400,
            detail="Não foi possível adicionar arquivo"
        ) 
    db.refresh(novo_artigo)
    return novo_artigo

def atualizar_artigo_pelo_id(id:int,db:Session,artigo_input:artigos.Artigo):
    artigo = db.query(
        Artigo
        ).filter(
           Artigo.deletado==None,Artigo.id == id
            ).first()
    if artigo ==None:
        raise HTTPException(
            status_code=204,
            detail="Artigo não encontrado"
        )
    if artigo_input.title !=None:
        artigo.title = artigo_input.title
    if artigo_input.url !=None:
        artigo.url = artigo_input.url 
    if artigo_input.image_url !=None:
        artigo.image_url = artigo_input.image_url 
    if artigo_input.news_site !=None:
        artigo.news_site = artigo_input.news_site
    if artigo_input.summary !=None:
        artigo.summary = artigo_input.summary
    if artigo_input.publishiedAt !=None:
        artigo.publishiedAt = artigo_input.publishiedAt 
    db.commit()
    db.refresh(artigo)
    return artigo

def deletar_artigo_pelo_id(id:int,db:Session):
    artigo = db.query(
        Artigo
        ).filter(
           Artigo.deletado==None,Artigo.id == id
            ).first()
    if artigo ==None:
        raise HTTPException(
            status_code=204,
            detail="Artigo não encontrado"
        )
    artigo.deletado = datetime.datetime.now()
    db.commit()
    db.refresh(artigo)
    return True
