from database import conectar
from models.vinculo import Vinculo

def inserir_vinculo(mat_estudante, curso_id, data_entrada, status):
    try:
        Vinculo(mat_estudante, curso_id, data_entrada, status).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Usamos as colunas exatas do dump do banco (curso, data_entrada, status)
            query = """
                INSERT INTO universidade.vinculo (mat_estudante, curso, data_entrada, status) 
                VALUES (%s, %s, %s, %s) RETURNING idVinculo;
            """
            
            cursor.execute(query, (mat_estudante, curso_id, data_entrada, status))
            id_gerado = cursor.fetchone()[0]
            conn.commit()
            print(f"\n[OK] Vínculo criado! ID do Vínculo: {id_gerado} | Matrícula: {mat_estudante}")
            
        except Exception as e:
            print(f"\n[ERRO] Falha ao criar vínculo. Verifique os dados:\n{e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def listar_vinculos():
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Correção feita no JOIN: v.curso = c.idCurso
            query = """
                SELECT v.idVinculo, v.mat_estudante, u.nome, c.nome AS curso, v.status 
                FROM universidade.vinculo v
                JOIN universidade.estudante e ON v.mat_estudante = e.mat_estudante
                JOIN universidade.usuario u ON e.cpf = u.cpf
                JOIN universidade.curso c ON v.curso = c.idCurso
                ORDER BY v.idVinculo;
            """
            
            cursor.execute(query)
            vinculos = cursor.fetchall()
            
            print("\n--- Relatório de Matrículas (Vínculos) ---")
            for v in vinculos:
                print(f"ID Vínculo: {v[0]} | Matrícula: {v[1]} | Aluno: {v[2]} | Curso: {v[3]} | Status: {v[4]}")
            print("------------------------------------------")
            
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar vínculos: {e}")
        finally:
            cursor.close()
            conn.close()

def deletar_vinculo(id_vinculo):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM universidade.vinculo WHERE idVinculo = %s;"
            cursor.execute(query, (id_vinculo,))
            
            if cursor.rowcount == 0:
                print(f"\n[AVISO] Nenhum vínculo encontrado com o ID {id_vinculo}.")
            else:
                conn.commit()
                print(f"\n[OK] Vínculo ID {id_vinculo} removido com sucesso!")
                
        except Exception as e:
            print(f"\n[ERRO] Falha ao remover vínculo: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()