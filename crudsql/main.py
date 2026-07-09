import crud_usuario
import crud_curso
import crud_estudante
import crud_vinculo
from models.curso import GRAUS, TURNOS, NIVEIS
from models.vinculo import STATUS


def escolher_enum(titulo, opcoes):
    print(f"\n{titulo}:")
    for i, op in enumerate(opcoes, 1):
        print(f"  {i}. {op}")
    while True:
        try:
            idx = int(input("  Escolha o número: ")) - 1
            if 0 <= idx < len(opcoes):
                return opcoes[idx]
            print("  [AVISO] Número fora do intervalo.")
        except ValueError:
            print("  [AVISO] Digite um número válido.")


def input_lista(prompt):
    entrada = input(prompt).strip()
    if not entrada:
        return None
    return [item.strip() for item in entrada.split(',')]


def input_inteiro(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  [AVISO] Digite um número inteiro válido.")


def input_decimal(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  [AVISO] Digite um número decimal válido.")


def input_data(prompt):
    valor = input(prompt).strip()
    return valor if valor else None


def separador(titulo):
    print("\n" + "=" * 38)
    print(f"  {titulo}")
    print("=" * 38)


def menu_usuarios():
    while True:
        separador("USUÁRIOS")
        print("1. Listar todos")
        print("2. Inserir")
        print("3. Atualizar")
        print("4. Deletar")
        print("0. Voltar")
        op = input("\nOpção: ").strip()

        if op == '1':
            crud_usuario.listar_usuarios()

        elif op == '2':
            print("\n--- Novo Usuário ---")
            cpf            = input("CPF (somente números): ").strip()
            nome           = input("Nome completo: ").strip()
            data_nasc      = input_data("Data de nascimento (AAAA-MM-DD): ")
            emails         = input_lista("E-mails (separados por vírgula, ou Enter para nenhum): ")
            telefones      = input_lista("Telefones (separados por vírgula, ou Enter para nenhum): ")
            login          = input("Login: ").strip()
            senha          = input("Senha: ").strip()
            crud_usuario.inserir_usuario(cpf, nome, data_nasc, emails, telefones, login, senha)

        elif op == '3':
            print("\n--- Atualizar Usuário ---")
            cpf            = input("CPF do usuário: ").strip()
            nome           = input("Novo nome completo: ").strip()
            data_nasc      = input_data("Nova data de nascimento (AAAA-MM-DD): ")
            emails         = input_lista("Novos e-mails (separados por vírgula, ou Enter para nenhum): ")
            telefones      = input_lista("Novos telefones (separados por vírgula, ou Enter para nenhum): ")
            login          = input("Novo login: ").strip()
            senha          = input("Nova senha: ").strip()
            crud_usuario.atualizar_usuario(cpf, nome, data_nasc, emails, telefones, login, senha)

        elif op == '4':
            print("\n--- Deletar Usuário ---")
            cpf = input("CPF do usuário a deletar: ").strip()
            crud_usuario.deletar_usuario(cpf)

        elif op == '0':
            break
        else:
            print("\n[ERRO] Opção inválida.")


def menu_cursos():
    while True:
        separador("CURSOS")
        print("1. Listar todos")
        print("2. Inserir")
        print("3. Atualizar")
        print("4. Deletar")
        print("0. Voltar")
        op = input("\nOpção: ").strip()

        if op == '1':
            crud_curso.listar_cursos()

        elif op == '2':
            print("\n--- Novo Curso ---")
            nome   = input("Nome do curso: ").strip()
            grau   = escolher_enum("Grau", GRAUS)
            turno  = escolher_enum("Turno", TURNOS)
            campus = input("Campus: ").strip()
            nivel  = escolher_enum("Nível", NIVEIS)
            crud_curso.inserir_curso(nome, grau, turno, campus, nivel)

        elif op == '3':
            print("\n--- Atualizar Curso ---")
            id_curso = input_inteiro("ID do curso a atualizar: ")
            nome     = input("Novo nome: ").strip()
            grau     = escolher_enum("Novo grau", GRAUS)
            turno    = escolher_enum("Novo turno", TURNOS)
            campus   = input("Novo campus: ").strip()
            nivel    = escolher_enum("Novo nível", NIVEIS)
            crud_curso.atualizar_curso(id_curso, nome, grau, turno, campus, nivel)

        elif op == '4':
            print("\n--- Deletar Curso ---")
            id_curso = input_inteiro("ID do curso a deletar: ")
            crud_curso.deletar_curso(id_curso)

        elif op == '0':
            break
        else:
            print("\n[ERRO] Opção inválida.")


def menu_estudantes():
    while True:
        separador("ESTUDANTES")
        print("1. Listar todos")
        print("2. Inserir")
        print("3. Atualizar (MC e ano de ingresso)")
        print("4. Deletar")
        print("0. Voltar")
        op = input("\nOpção: ").strip()

        if op == '1':
            crud_estudante.listar_estudantes()

        elif op == '2':
            print("\n--- Novo Estudante ---")
            mat          = input("Matrícula (ex: E114): ").strip()
            cpf          = input("CPF (somente números, deve existir em Usuários): ").strip()
            mc           = input_decimal("MC (média de créditos): ")
            ano_ingresso = input_inteiro("Ano de ingresso: ")
            crud_estudante.inserir_estudante(mat, cpf, mc, ano_ingresso)

        elif op == '3':
            print("\n--- Atualizar Estudante ---")
            mat          = input("Matrícula do estudante: ").strip()
            mc           = input_decimal("Nova MC: ")
            ano_ingresso = input_inteiro("Novo ano de ingresso: ")
            crud_estudante.atualizar_estudante(mat, mc, ano_ingresso)

        elif op == '4':
            print("\n--- Deletar Estudante ---")
            mat = input("Matrícula do estudante a deletar: ").strip()
            crud_estudante.deletar_estudante(mat)

        elif op == '0':
            break
        else:
            print("\n[ERRO] Opção inválida.")


def menu_vinculos():
    while True:
        separador("VÍNCULOS / MATRÍCULAS")
        print("1. Listar todos")
        print("2. Inserir")
        print("3. Deletar")
        print("0. Voltar")
        op = input("\nOpção: ").strip()

        if op == '1':
            crud_vinculo.listar_vinculos()

        elif op == '2':
            print("\n--- Novo Vínculo ---")
            crud_curso.listar_cursos()
            mat          = input("Matrícula do estudante: ").strip()
            curso_id     = input_inteiro("ID do curso: ")
            data_entrada = input_data("Data de entrada (AAAA-MM-DD, ou Enter para nulo): ")
            status       = escolher_enum("Status", STATUS)
            crud_vinculo.inserir_vinculo(mat, curso_id, data_entrada, status)

        elif op == '3':
            print("\n--- Deletar Vínculo ---")
            crud_vinculo.listar_vinculos()
            id_vinculo = input_inteiro("ID do vínculo a deletar: ")
            crud_vinculo.deletar_vinculo(id_vinculo)

        elif op == '0':
            break
        else:
            print("\n[ERRO] Opção inválida.")


def main():
    while True:
        separador("SISTEMA ACADÊMICO - POSTGRESQL")
        print("1. Usuários")
        print("2. Cursos")
        print("3. Estudantes")
        print("4. Vínculos / Matrículas")
        print("0. Sair")
        op = input("\nOpção: ").strip()

        if op == '1':
            menu_usuarios()
        elif op == '2':
            menu_cursos()
        elif op == '3':
            menu_estudantes()
        elif op == '4':
            menu_vinculos()
        elif op == '0':
            print("\nEncerrando o sistema. Até logo!\n")
            break
        else:
            print("\n[ERRO] Opção inválida.")


if __name__ == "__main__":
    main()