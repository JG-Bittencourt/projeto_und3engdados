import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv(override=True)

def conectar():
    """Retorna a instância do banco de dados MongoDB conectado."""
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "universidade_nosql")
    
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        
        return client[db_name]
    
    except Exception as e:
        print(f"\n[ERRO FATAL DE CONEXÃO] Não foi possível conectar ao MongoDB Atlas:\n{e}")
        return None

if __name__ == "__main__":
    print("Testando a conexão com o MongoDB Atlas na AWS...")
    db = conectar()
    if db is not None:
        print(f"[OK] Conexão com o banco '{db.name}' estabelecida com sucesso!")