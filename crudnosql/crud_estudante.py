from database import conectar
from models.estudante import Estudante

def inserir_estudante(mat_estudante, cpf, mc, ano_ingresso):
    try:
        Estudante(mat_estudante, cpf, mc, ano_ingresso).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    db = conectar()
    if db is not None:
        try:
           
            if db.estudante.find_one({"mat_estudante": mat_estudante}):
                print(f"\n[ERRO] A matrícula '{mat_estudante}' já existe!")
                return
            
            
            if not db.usuario.find_one({"cpf": cpf}):
                print(f"\n[ERRO] Violação de Integridade! O CPF '{cpf}' não está cadastrado em Usuários.")
                return

            novo_estudante = {
                "mat_estudante": mat_estudante,
                "cpf": cpf,
                "MC": mc,
                "ano_ingresso": ano_ingresso
            }
            db.estudante.insert_one(novo_estudante)
            print(f"\n[OK] Estudante matrícula '{mat_estudante}' inserido com sucesso!")
            
        except Exception as e:
            print(f"\n[ERRO] Falha ao inserir estudante: {e}")

def listar_estudantes():
    db = conectar()
    if db is not None:
        try:
            
            pipeline = [
                {
                    "$lookup": {
                        "from": "usuario",           
                        "localField": "cpf",         
                        "foreignField": "cpf",       
                        "as": "dados_usuario"        
                    }
                },
                {"$sort": {"mat_estudante": 1}}
            ]
            
            estudantes = list(db.estudante.aggregate(pipeline))
            
            print("\n--- Estudantes Cadastrados ---")
            for e in estudantes:
               
                nome_usuario = e['dados_usuario'][0]['nome'] if e.get('dados_usuario') else "Desconhecido"
                
                print(f"Matrícula: {e.get('mat_estudante')} | Nome: {nome_usuario} | CPF: {e.get('cpf')} | MC: {e.get('MC')} | Ingresso: {e.get('ano_ingresso')}")
            print("------------------------------")
            return estudantes
            
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar estudantes: {e}")

def atualizar_estudante(mat_estudante, mc, ano_ingresso):
    try:
        Estudante(mat_estudante, '00000000000', mc, ano_ingresso).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    db = conectar()
    if db is not None:
        try:
            novos_dados = {"$set": {"MC": mc, "ano_ingresso": ano_ingresso}}
            resultado = db.estudante.update_one({"mat_estudante": mat_estudante}, novos_dados)
            
            if resultado.matched_count == 0:
                print(f"\n[AVISO] Nenhum estudante com a matrícula {mat_estudante}.")
            else:
                print(f"\n[OK] Estudante {mat_estudante} atualizado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao atualizar estudante: {e}")

def deletar_estudante(mat_estudante):
    db = conectar()
    if db is not None:
        try:
            resultado = db.estudante.delete_one({"mat_estudante": mat_estudante})
            if resultado.deleted_count == 0:
                print(f"\n[AVISO] Nenhum estudante encontrado com a matrícula {mat_estudante}.")
            else:
                print(f"\n[OK] Estudante {mat_estudante} deletado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao deletar estudante: {e}")