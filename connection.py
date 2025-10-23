from sqlalchemy import create_engine



# variavels para entrar no banco
HOST='127.0.0.1' #host padrao
PORT='3306' #porta padrao
USER='root' # usuario padrao
DB='petamigos' # nome do banco, criado diretamente no sql

SQLALCHEMY_DATABASE_URI =f"mysql+pymysql://{USER}@{HOST}/{DB}" #URI de conexão do sqlalchemy, usando mysql+pymysql, utilizando as variaveis do banco
SQLALCHEMY_TRACK_MODIFICATIONS = False

# cria a engine, ou seja a ponte de conexão usando a URI
engine = create_engine(SQLALCHEMY_DATABASE_URI)


# try para testar a conexão
try:
    # cria a variavel connection que recebe o engine(ponte) para fazer a conexão com o metodo .connect()
    connection = engine.connect()
    print("banco conectado")

except Exception as e:
    print(f"falha ao conectar {e}")