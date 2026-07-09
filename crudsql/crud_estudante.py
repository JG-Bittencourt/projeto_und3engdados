from database import conectar
from models.estudante import Estudante

def inserir_estudante(mat_estudante, cpf, mc, ano_ingresso):
    try:
        Estudante(mat_estudante, cpf, mc, ano_ingresso).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO universidade.estudante (mat_estudante, cpf, MC, ano_ingresso) 
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (mat_estudante, cpf, mc, ano_ingresso))
            conn.commit()
            print(f"\n[OK] Estudante matrícula '{mat_estudante}' inserido com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao inserir estudante (Verifique se o CPF existe):\n{e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def listar_estudantes():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT e.mat_estudante, u.nome, e.cpf, e.MC, e.ano_ingresso 
                FROM universidade.estudante e
                JOIN universidade.usuario u ON e.cpf = u.cpf
                ORDER BY e.mat_estudante;
            """
            cursor.execute(query)
            estudantes = cursor.fetchall()
            
            print("\n--- Estudantes Cadastrados ---")
            for e in estudantes:
                print(f"Matrícula: {e[0]} | Nome: {e[1]} | CPF: {e[2]} | MC: {e[3]} | Ingresso: {e[4]}")
            print("------------------------------")
            return estudantes
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar estudantes: {e}")
        finally:
            cursor.close()
            conn.close()

def atualizar_estudante(mat_estudante, mc, ano_ingresso):
    try:
        Estudante(mat_estudante, '00000000000', mc, ano_ingresso).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE universidade.estudante 
                SET MC = %s, ano_ingresso = %s
                WHERE mat_estudante = %s;
            """
            cursor.execute(query, (mc, ano_ingresso, mat_estudante))
            
            if cursor.rowcount == 0:
                print(f"\n[AVISO] Nenhum estudante com a matrícula {mat_estudante}.")
            else:
                conn.commit()
                print(f"\n[OK] Estudante {mat_estudante} atualizado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao atualizar estudante: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def deletar_estudante(mat_estudante):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM universidade.estudante WHERE mat_estudante = %s;"
            cursor.execute(query, (mat_estudante,))
            
            if cursor.rowcount == 0:
                print(f"\n[AVISO] Nenhum estudante encontrado com a matrícula {mat_estudante}.")
            else:
                conn.commit()
                print(f"\n[OK] Estudante {mat_estudante} deletado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao deletar estudante: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()