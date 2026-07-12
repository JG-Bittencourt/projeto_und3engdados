GRAUS  = ['Bacharelado', 'Licenciatura Plena']
TURNOS = ['Matutino', 'Vespertino', 'Noturno', 'Turno Indefinido']
NIVEIS = ['Graduação', 'Mestrado', 'Doutorado', 'Lato']


class Curso:
    def __init__(self, nome, grau, turno, campus, nivel):
        self.nome   = nome.strip() if nome else None
        self.grau   = grau
        self.turno  = turno
        self.campus = campus.strip() if campus else None
        self.nivel  = nivel

    def validar(self):
        erros = []

        if not self.nome or len(self.nome) < 3:
            erros.append("Nome do curso inválido: mínimo 3 caracteres.")

        if self.grau not in GRAUS:
            erros.append(f"Grau inválido. Valores aceitos: {', '.join(GRAUS)}")

        if self.turno not in TURNOS:
            erros.append(f"Turno inválido. Valores aceitos: {', '.join(TURNOS)}")

        if not self.campus or len(self.campus) < 2:
            erros.append("Campus inválido: mínimo 2 caracteres.")

        if self.nivel not in NIVEIS:
            erros.append(f"Nível inválido. Valores aceitos: {', '.join(NIVEIS)}")

        if erros:
            raise ValueError("\n".join(f"  - {e}" for e in erros))