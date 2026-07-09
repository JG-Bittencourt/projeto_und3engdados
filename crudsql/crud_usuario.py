from database import conectar
from models.usuario import Usuario

def inserir_usuario(cpf, nome, data_nascimento, emails, telefones, login, senha):
    try:
        Usuario(cpf, nome, data_nascimento, emails, telefones, login, senha).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO universidade.usuario (cpf, nome, data_nascimento, email, telefone, login, senha)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (cpf, nome, data_nascimento, emails, telefones, login, senha))
            conn.commit()
            print(f"\n[OK] Usuário '{nome}' (CPF: {cpf}) inserido com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao inserir o usuário: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def listar_usuarios():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT cpf, nome, data_nascimento, email, telefone, login
                FROM universidade.usuario
                ORDER BY cpf
            """
            cursor.execute(query)
            usuarios = cursor.fetchall()
            print("\n----------Usuários Cadastrados----------")
            for u in usuarios:
                print(f"CPF: {u[0]} | NOME: {u[1]} | NASC: {u[2]} | EMAIL: {u[3]} | TELEFONE: {u[4]} | LOGIN: {u[5]}")
            print("----------------------------------------")
            return usuarios
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar usuários: {e}")
        finally:
            cursor.close()
            conn.close()

def atualizar_usuario(cpf, nome, data_nascimento, emails, telefones, login, senha):
    try:
        Usuario(cpf, nome, data_nascimento, emails, telefones, login, senha).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE universidade.usuario
                SET nome = %s, data_nascimento = %s, email = %s, telefone = %s, login = %s, senha = %s
                WHERE cpf = %s
            """
            cursor.execute(query, (nome, data_nascimento, emails, telefones, login, senha, cpf))
            if cursor.rowcount == 0:
                print(f"\n[AVISO] Nenhum usuário encontrado com o CPF {cpf}.")
            else:
                conn.commit()
                print(f"\n[OK] Usuário CPF {cpf} atualizado com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao atualizar usuário: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def deletar_usuario(cpf):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM universidade.usuario WHERE cpf = %s"
            cursor.execute(query, (cpf,))
            if cursor.rowcount == 0:
                print(f"\n[AVISO] Nenhum usuário encontrado com o CPF {cpf}.")
            else:
                conn.commit()
                print(f"\n[OK] Usuário CPF {cpf} deletado com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao deletar usuário: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()