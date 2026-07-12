from database import conectar
from models.curso import Curso

def inserir_curso(nome, grau, turno, campus, nivel):
    try:
        Curso(nome, grau, turno, campus, nivel).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    db = conectar()
    if db is not None:
        try:
            # LÓGICA DE AUTO-INCREMENTO (Substitui o SERIAL do SQL)
            # Busca o curso com o maior idCurso. Se não achar nada, começa com 1.
            ultimo_curso = db.curso.find_one(sort=[("idCurso", -1)])
            novo_id = ultimo_curso["idCurso"] + 1 if ultimo_curso else 1

            novo_curso = {
                "idCurso": novo_id,
                "nome": nome,
                "grau": grau,
                "turno": turno,
                "campus": campus,
                "nivel": nivel
            }
            
            db.curso.insert_one(novo_curso)
            print(f"\n[OK] Curso '{nome}' inserido com sucesso! ID gerado: {novo_id}")
        except Exception as e:
            print(f"\n[ERRO] Falha ao inserir o curso: {e}")

def listar_cursos():
    db = conectar()
    if db is not None:
        try:
            # Busca todos e ordena de forma crescente pelo idCurso (1)
            cursos = list(db.curso.find().sort("idCurso", 1))
            
            print("\n--- Cursos Cadastrados ---")
            for c in cursos:
                print(f"ID: {c.get('idCurso')} | Nome: {c.get('nome')} | Grau: {c.get('grau')} | Turno: {c.get('turno')} | Campus: {c.get('campus')} | Nível: {c.get('nivel')}")
            print("--------------------------")
            return cursos
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar cursos: {e}")

def atualizar_curso(id_curso, nome, grau, turno, campus, nivel):
    try:
        Curso(nome, grau, turno, campus, nivel).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    db = conectar()
    if db is not None:
        try:
            novos_dados = {
                "$set": {
                    "nome": nome,
                    "grau": grau,
                    "turno": turno,
                    "campus": campus,
                    "nivel": nivel
                }
            }
            
            resultado = db.curso.update_one({"idCurso": id_curso}, novos_dados)
            
            if resultado.matched_count == 0:
                print(f"\n[AVISO] Nenhum curso com o ID {id_curso}.")
            else:
                print(f"\n[OK] Curso ID {id_curso} atualizado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao atualizar curso: {e}")

def deletar_curso(id_curso):
    db = conectar()
    if db is not None:
        try:
            resultado = db.curso.delete_one({"idCurso": id_curso})
            
            if resultado.deleted_count == 0:
                print(f"\n[AVISO] Nenhum curso encontrado com o ID {id_curso}.")
            else:
                print(f"\n[OK] Curso ID {id_curso} deletado.")
        except Exception as e:
            print(f"\n[ERRO] Falha ao deletar curso: {e}")