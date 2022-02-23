
from typing import List
from starlette.status import  HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from dependencias import *
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from crud import artigos

from schemas import artigos as schema
descricao = """
This is a challenge by Coodesh🚀

## Artigos

Selecionar todos os **artigos** de forma paginada.
* **Selecionar artigo específico** .
* **Modificar artigo específico** .
* **Adicionar artigo** .
* **Deletar artigo espcífico** .

"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app =  FastAPI(version="0.0.1",
title="Spack Flight Challenger News!",
contact={"name":"Javier Salvador","email":"javiersrf@gmail.com"},
description= descricao)
#-----------------------------------------------------------------------------------------------------------------------
#Espaço separado para as rotas
#-----------------------------------------------------------------------------------------------------------------------
#------------------ROTA INICIAL APRESENTACAO-----------------------------------------------------------------------------------------------------

## ponto raíz da aplicação trazendo as informações globais
@app.get("/",status_code=200)
async def root():
    return "Back-end Challenge 2021 🏅 - Space Flight News"


@app.get("/articles/",status_code=200,response_model=List[schema.Artigo])
async def selecionar_todos_os_artigos(pagina:int = 1,db = Depends(get_db)):
    resposta = artigos.get_todos_artigos(db,pagina)
    return resposta 

@app.post("/articles/",status_code=200,response_model=schema.Artigo)
async def postar_novo_artigo(novo_artigo:schema.Artigo,db = Depends(get_db)):
    resposta = artigos.insert_novo_artigo(db,novo_artigo)
    return resposta 

@app.get("/articles/{id}",status_code=200,response_model=schema.Artigo)
async def selecionar_artigo_pleo_id(id:int,db = Depends(get_db)):
    resposta = artigos.get_artigo_pelo_id(id,db)
    return resposta

@app.put("/articles/{id}",status_code=200,response_model=schema.Artigo)
async def modificar_artigo_pelo_id(db = Depends(get_db)):
    resposta = artigos.atualizar_artigo_pelo_id(id,db,schema.Artigo)
    return resposta

@app.delete("/articles/{id}",status_code=200)
async def delete_artigo(db = Depends(get_db)):
    resposta = artigos.deletar_artigo_pelo_id(id,db,schema.Artigo)
    return "Artigo deletado com sucesso"


