from database import conectar
from models.vinculo import Vinculo

def inserir_vinculo(mat_estudante, curso_id, data_entrada, status):
    try:
        Vinculo(mat_estudante, curso_id, data_entrada, status).validar()
    except ValueError as e:
        print(f"\n[INVÁLIDO]\n{e}")
        return

    db = conectar()
    if db is not None:
        try:
            # 1. VALIDAÇÃO DE CHAVES ESTRANGEIRAS
            if not db.estudante.find_one({"mat_estudante": mat_estudante}):
                print(f"\n[ERRO] Matrícula '{mat_estudante}' não encontrada! Cadastro cancelado.")
                return
                
            if not db.curso.find_one({"idCurso": curso_id}):
                print(f"\n[ERRO] Curso ID '{curso_id}' não encontrado! Cadastro cancelado.")
                return

            # 2. LÓGICA DE AUTO-INCREMENTO
            ultimo_vinculo = db.vinculo.find_one(sort=[("idVinculo", -1)])
            novo_id = ultimo_vinculo["idVinculo"] + 1 if ultimo_vinculo else 1

            # 3. INSERÇÃO
            novo_vinculo = {
                "idVinculo": novo_id,
                "mat_estudante": mat_estudante,
                "curso": curso_id,
                "data_entrada": data_entrada,
                "status": status
            }
            
            db.vinculo.insert_one(novo_vinculo)
            print(f"\n[OK] Vínculo criado! ID do Vínculo: {novo_id} | Matrícula: {mat_estudante}")
            
        except Exception as e:
            print(f"\n[ERRO] Falha ao criar vínculo. Verifique os dados:\n{e}")

def listar_vinculos():
    db = conectar()
    if db is not None:
        try:
            # Pipeline de Aggregation (Equivalente ao JOIN triplo do SQL)
            pipeline = [
                # JOIN com estudante
                {"$lookup": {
                    "from": "estudante",
                    "localField": "mat_estudante",
                    "foreignField": "mat_estudante",
                    "as": "dados_estudante"
                }},
                {"$unwind": {"path": "$dados_estudante", "preserveNullAndEmptyArrays": True}},
                
                # JOIN com usuario (usando o CPF que veio do estudante)
                {"$lookup": {
                    "from": "usuario",
                    "localField": "dados_estudante.cpf",
                    "foreignField": "cpf",
                    "as": "dados_usuario"
                }},
                {"$unwind": {"path": "$dados_usuario", "preserveNullAndEmptyArrays": True}},
                
                # JOIN com curso
                {"$lookup": {
                    "from": "curso",
                    "localField": "curso",
                    "foreignField": "idCurso",
                    "as": "dados_curso"
                }},
                {"$unwind": {"path": "$dados_curso", "preserveNullAndEmptyArrays": True}},
                
                # ORDER BY idVinculo
                {"$sort": {"idVinculo": 1}}
            ]
            
            vinculos = list(db.vinculo.aggregate(pipeline))
            
            print("\n--- Relatório de Matrículas (Vínculos) ---")
            for v in vinculos:
                # Tratamento para evitar quebra caso dados_usuario ou dados_curso sejam nulos
                aluno_nome = v.get("dados_usuario", {}).get("nome", "Desconhecido")
                curso_nome = v.get("dados_curso", {}).get("nome", "Desconhecido")
                
                print(f"ID Vínculo: {v.get('idVinculo')} | Matrícula: {v.get('mat_estudante')} | Aluno: {aluno_nome} | Curso: {curso_nome} | Status: {v.get('status')}")
            print("------------------------------------------")
            
        except Exception as e:
            print(f"\n[ERRO] Falha ao listar vínculos: {e}")

def deletar_vinculo(id_vinculo):
    db = conectar()
    if db is not None:
        try:
            resultado = db.vinculo.delete_one({"idVinculo": id_vinculo})
            
            if resultado.deleted_count == 0:
                print(f"\n[AVISO] Nenhum vínculo encontrado com o ID {id_vinculo}.")
            else:
                print(f"\n[OK] Vínculo ID {id_vinculo} removido com sucesso!")
                
        except Exception as e:
            print(f"\n[ERRO] Falha ao remover vínculo: {e}")