import psycopg2
import requests
from requests import Response
from config_db import DATABASE,HOST_DATABASE,PASSWORD,USER
import schedule
import time
def error_no_codigo():
    print("Error ")
def carregar_dados():
    '''
    Verificando qual o maior id que já existe no banco
    '''
    _start = 0
   
    connPg = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST_DATABASE)
    with connPg.cursor() as pgconexao:
            pgconexao.execute(
                """
                SELECT id FROM dbartigos
                ORDER BY id desc
                limit 1;
                """
            )
            resultado = pgconexao.fetchone()
            if resultado !=None:
                _start = resultado[0]
    response:Response = requests.get("https://api.spaceflightnewsapi.net/v3/articles/count")
    if response.status_code != 200:
        error_no_codigo()
    quantidade_de_artigos = response.json()
    
    response = requests.get(f"https://api.spaceflightnewsapi.net/v3/articles/?_limit={quantidade_de_artigos}&_start={_start}")
    artigos_resultado = response.json()

    for artigo in artigos_resultado:
        comando="""INSERT INTO dbartigos(
            "id","featured","title","url","image_url","news_site","summary","publishiedat") VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s)"""
        with connPg.cursor() as pgconexao:
            pgconexao.execute(comando,(str(artigo["id"]),1 if artigo["featured"] else 0,artigo["title"],artigo["url"],artigo["imageUrl"],artigo["newsSite"],artigo["summary"],artigo["publishedAt"]))
            for laucher in artigo["launches"]:
                pgconexao.execute("""
                INSERT INTO artigos_lauchers(
                "id","id_artigo","provider") VALUES
                (%s,%s,%s)""",(laucher["id"],artigo["id"],laucher["provider"]))
            for evento in artigo["events"]:
                pgconexao.execute(f"""
                INSERT INTO artigos_events(
                "id","id_artigo","provider") VALUES
                (%s,%s,%s)""",(evento["id"],str(artigo["id"]),evento["provider"]))
            connPg.commit()

    
    


if __name__ == "__main__":
    carregar_dados()
    schedule.every().day.at("21:00").do(carregar_dados)
    while True:
        schedule.run_pending()
        time.sleep(1)