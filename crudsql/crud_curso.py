from database import conectar
from models.curso import Curso

def inserir_curso(nome, grau, turno, campus, nivel):
    try:
        Curso(nome, grau, turno, campus, nivel).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """ INSERT INTO universidade.curso (nome, grau, turno, campus, nivel) VALUES (%s, %s, %s, %s, %s) RETURNING idCurso;"""
            cursor.execute(query, (nome,grau,turno,campus,nivel))
            id_gerado = cursor.fetchone()[0]
            conn.commit()
            print(f"\n[OK] Curso '{nome}' inserido com sucesso!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao inserir o curso.")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def listar_cursos():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """SELECT idCurso, nome, grau, turno, campus, nivel FROM universidade.curso ORDER BY idCurso"""
            cursor.execute(query)
            cursos = cursor.fetchall()
            
            print("\n--- Cursos Cadastrados ---")
            for c in cursos:
                print(f"ID: {c[0]} | Nome: {c[1]} | Grau: {c[2]} | Turno: {c[3]} | Campus: {c[4]} | Nível: {c[5]}")
            print("--------------------------")
            return cursos
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar cursos: {e}")
        finally:
            cursor.close()
            conn.close()

def atualizar_curso(id_curso, nome, grau, turno, campus, nivel):
    try:
        Curso(nome, grau, turno, campus, nivel).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                UPDATE universidade.curso 
                SET nome = %s, grau = %s, turno = %s, campus = %s, nivel = %s
                WHERE idCurso = %s;
            """
            cursor.execute(query, (nome, grau, turno, campus, nivel, id_curso))
            
            if cursor.rowcount == 0:
                print(f"\n[AVISO] Nenhum curso com o ID {id_curso}.")
            else:
                conn.commit()
                print(f"\n[OK] Curso ID {id_curso} atualizado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao atualizar curso: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def deletar_curso(id_curso):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM universidade.curso WHERE idCurso = %s;"
            cursor.execute(query, (id_curso,))
            
            if cursor.rowcount == 0:
                print(f"\n[AVISO] Nenhum curso encontrado com o ID {id_curso}.")
            else:
                conn.commit()
                print(f"\n[OK] Curso ID {id_curso} deletado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao deletar curso: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()