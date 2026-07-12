class Usuario:
    def __init__(self, cpf, nome, data_nascimento, emails, telefones, login, senha):
        self.cpf            = str(cpf).strip() if cpf else None
        self.nome           = nome.strip() if nome else None
        self.data_nascimento = data_nascimento or None
        self.emails         = emails or []
        self.telefones      = telefones or []
        self.login          = login.strip() if login else None
        self.senha          = senha

    def validar(self):
        erros = []

        if not self.cpf or not self.cpf.isdigit():
            erros.append("CPF inválido: deve conter apenas números.")
        elif len(self.cpf) != 11:
            erros.append("CPF inválido: deve ter exatamente 11 dígitos.")

        if not self.nome or len(self.nome) < 3:
            erros.append("Nome inválido: mínimo 3 caracteres.")

        if not self.login or len(self.login) < 3:
            erros.append("Login inválido: mínimo 3 caracteres.")

        if not self.senha or len(self.senha) < 6:
            erros.append("Senha inválida: mínimo 6 caracteres.")

        if self.emails and not isinstance(self.emails, list):
            erros.append("E-mails devem ser uma lista.")

        if self.telefones and not isinstance(self.telefones, list):
            erros.append("Telefones devem ser uma lista.")

        if erros:
            raise ValueError("\n".join(f"  - {e}" for e in erros))