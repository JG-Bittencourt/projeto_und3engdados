import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return conn
    
    except psycopg2.OperationalError as e:
        print(f"\n[ERRO FATAL DE CONEXÃO] Não foi possível conectar ao banco de dados:\n{e}")
        print("Verifique se o serviço do PostgreSQL está rodando e se os dados no .env estão corretas.")
        return None
    
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
        return None
    

if __name__ == "__main__":
    print("Testando a conexão com o banco de dados local...")
    conexao = conectar()
    
    if conexao:
        print("[OK] Conexão com o PostgreSQL estabelecida com sucesso!")
        conexao.close()
    else:
        print("[FALHA] A conexão não pôde ser estabelecida.")