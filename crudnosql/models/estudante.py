from datetime import datetime


class Estudante:
    def __init__(self, mat_estudante, cpf, mc, ano_ingresso):
        self.mat_estudante = mat_estudante.strip() if mat_estudante else None
        self.cpf           = str(cpf).strip() if cpf else None
        self.mc            = mc
        self.ano_ingresso  = ano_ingresso

    def validar(self):
        erros = []

        if not self.mat_estudante:
            erros.append("Matrícula não informada.")

        if not self.cpf or not self.cpf.isdigit():
            erros.append("CPF inválido: deve conter apenas números.")

        if self.mc is None:
            erros.append("MC não informada.")
        else:
            try:
                mc = float(self.mc)
                if not (0.0 <= mc <= 10.0):
                    erros.append("MC inválida: deve ser entre 0.0 e 10.0.")
            except (ValueError, TypeError):
                erros.append("MC inválida: deve ser um número.")

        ano_atual = datetime.now().year
        if self.ano_ingresso is None:
            erros.append("Ano de ingresso não informado.")
        else:
            try:
                ano = int(self.ano_ingresso)
                if not (1900 <= ano <= ano_atual):
                    erros.append(f"Ano de ingresso inválido: deve ser entre 1900 e {ano_atual}.")
            except (ValueError, TypeError):
                erros.append("Ano de ingresso inválido: deve ser um número inteiro.")

        if erros:
            raise ValueError("\n".join(f"  - {e}" for e in erros))