STATUS = ['Ativo', 'Cancelada', 'Formando', 'Graduado']


class Vinculo:
    def __init__(self, mat_estudante, curso_id, data_entrada, status):
        self.mat_estudante = mat_estudante.strip() if mat_estudante else None
        self.curso_id      = curso_id
        self.data_entrada  = data_entrada or None
        self.status        = status

    def validar(self):
        erros = []

        if not self.mat_estudante:
            erros.append("Matrícula não informada.")

        if self.curso_id is None:
            erros.append("ID do curso não informado.")
        else:
            try:
                if int(self.curso_id) <= 0:
                    erros.append("ID do curso inválido: deve ser maior que zero.")
            except (ValueError, TypeError):
                erros.append("ID do curso inválido: deve ser um número inteiro.")

        if self.status not in STATUS:
            erros.append(f"Status inválido. Valores aceitos: {', '.join(STATUS)}")

        if erros:
            raise ValueError("\n".join(f"  - {e}" for e in erros))