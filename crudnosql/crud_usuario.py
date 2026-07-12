from database import conectar
from models.usuario import Usuario

def inserir_usuario(cpf, nome, data_nascimento, emails, telefones, login, senha):
    try:
        Usuario(cpf, nome, data_nascimento, emails, telefones, login, senha).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    db = conectar()
    if db is not None:
        try:
            # RESTRIÇÃO DE CHAVE PRIMÁRIA: Garante que o CPF é único
            if db.usuario.find_one({"cpf": cpf}):
                print(f"\n[ERRO] O CPF '{cpf}' já está cadastrado no sistema!")
                return

            novo_usuario = {
                "cpf": cpf,
                "nome": nome,
                "data_nascimento": data_nascimento,
                "email": emails,      # No Mongo, podemos salvar a lista diretamente
                "telefone": telefones, # No Mongo, podemos salvar a lista diretamente
                "login": login,
                "senha": senha
            }
            db.usuario.insert_one(novo_usuario)
            print(f"\n[OK] Usuário '{nome}' (CPF: {cpf}) inserido com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao inserir o usuário: {e}")

def listar_usuarios():
    db = conectar()
    if db is not None:
        try:
            # .find() equivale ao SELECT * FROM, com sort() fazendo o ORDER BY
            usuarios = list(db.usuario.find().sort("cpf", 1))
            
            print("\n----------Usuários Cadastrados----------")
            for u in usuarios:
                print(f"CPF: {u.get('cpf')} | NOME: {u.get('nome')} | NASC: {u.get('data_nascimento')} | EMAIL: {u.get('email')} | LOGIN: {u.get('login')}")
            print("----------------------------------------")
            return usuarios
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar usuários: {e}")

def atualizar_usuario(cpf, nome, data_nascimento, emails, telefones, login, senha):
    try:
        Usuario(cpf, nome, data_nascimento, emails, telefones, login, senha).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    db = conectar()
    if db is not None:
        try:
            novos_dados = {
                "$set": {
                    "nome": nome,
                    "data_nascimento": data_nascimento,
                    "email": emails,
                    "telefone": telefones,
                    "login": login,
                    "senha": senha
                }
            }
            # update_one equivale ao UPDATE ... WHERE
            resultado = db.usuario.update_one({"cpf": cpf}, novos_dados)
            
            if resultado.matched_count == 0:
                print(f"\n[AVISO] Nenhum usuário encontrado com o CPF {cpf}.")
            else:
                print(f"\n[OK] Usuário CPF {cpf} atualizado com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao atualizar usuário: {e}")

def deletar_usuario(cpf):
    db = conectar()
    if db is not None:
        try:
            # delete_one equivale ao DELETE FROM ... WHERE
            resultado = db.usuario.delete_one({"cpf": cpf})
            
            if resultado.deleted_count == 0:
                print(f"\n[AVISO] Nenhum usuário encontrado com o CPF {cpf}.")
            else:
                print(f"\n[OK] Usuário CPF {cpf} deletado com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao deletar usuário: {e}")