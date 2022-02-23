from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
#conexão postgree 
engine =  create_engine("postgresql://epcdrhxnqlgulx:3d7dd2d5f87019572ff5eafc800bf689fabb18fde1933dd4bcfd12085f27fa4a@ec2-54-157-160-218.compute-1.amazonaws.com:5432/d5romauqfi3io")
SessionLocal = sessionmaker(autocommit=False,  bind=engine,)
