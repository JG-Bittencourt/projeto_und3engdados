# Trabalho Prático de Engenharia de Dados (2026.1)

**Instituição:** Universidade Federal de Sergipe (UFS)
**Disciplina:** Engenharia de Dados
**Professor:** André Britto de Carvalho
**Componentes do Grupo:** 
- João Vitor Vital Leão
- João Gustavo Costa Bittencourt Santos
- Lucca Pedreira Dultra

---

## 📌 Sobre o Projeto

Este repositório unificado contém a implementação das **Fases 1 e 2** do Trabalho Prático da disciplina. O objetivo geral consiste no desenvolvimento de aplicações que se comunicam com Sistemas de Gerenciamento de Bancos de Dados (SGBDs) relacionais e não relacionais, implementando operações de manipulação de dados em infraestrutura de nuvem (AWS).

### 📂 Estrutura do Repositório

```text
/
├── crudnosql/             # Código-fonte do CRUD em PostgreSQL
├── crudsql/               # Código-fonte do CRUD em MongoDB 
└── README.md              # Documentação geral
```

---

## 🗄️ Parte 1: CRUD Relacional (PostgreSQL)

A primeira etapa do trabalho focou no desenvolvimento de um programa para efetuar operações de CRUD (Create, Read, Update e Delete) no esquema relacional trabalhado em aula, especificamente nas tabelas: `usuario`, `estudante`, `vinculo` e `curso`.

* **SGBD:** PostgreSQL
* **Hospedagem:** AWS RDS (Relational Database Service)
* **Linguagem:** Python 3

### Como Executar a Parte 1
1. Navegue até o diretório da aplicação relacional: `cd parte1_sql`
2. Configure suas variáveis de ambiente no arquivo `.env` com as credenciais do AWS RDS.
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute o menu interativo: `python main.py`

---

## 🍃 Parte 2: Mapeamento e CRUD NoSQL (MongoDB)

A segunda etapa consistiu em migrar e representar todo o ecossistema do banco de dados relacional original (contendo 16 estruturas, incluindo disciplinas, turmas, departamentos, etc.) para o modelo orientado a documentos. Além do mapeamento, o programa em Python foi adaptado para realizar o CRUD das 4 entidades principais exigidas, comunicando-se com o banco não relacional.

* **SGBD:** MongoDB
* **Hospedagem:** Instância EC2 (Amazon Web Services)
* **Linguagem:** Python 3 (Biblioteca `pymongo`)

### Como Executar a Parte 2
1. Navegue até o diretório da aplicação NoSQL: `cd parte2_nosql`
2. Configure as variáveis de ambiente no arquivo `.env` apontando para o IP da instância EC2:
   ```env
   MONGO_URI="mongodb://usuario:senha@SEU_IP_AWS:27017/?authSource=admin"
   MONGO_DB_NAME="crudnosql"
   ```
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute o sistema: `python main.py`

### 🛡️ Tratamento de Restrições no NoSQL

Como o MongoDB não possui mecanismos nativos de Chaves Estrangeiras, a integridade do esquema mapeado foi garantida através da **lógica da aplicação**:

* **Restrição de Chave (PK e Unique):** Antes de qualquer inserção, o sistema executa validações via código (como `.find_one()`) utilizando os identificadores originais (`cpf`, `mat_estudante`, `idCurso`) para evitar duplicidade.
* **Integridade Referencial (FK):** A aplicação valida a presença de um documento "pai" antes de persistir o "filho". Exemplo: Não é possível cadastrar um `vinculo` se o `estudante` ou `curso` não existirem previamente na base.
* **Restrições de Domínio e NOT NULL:** O tratamento dos dados ocorre durante o preenchimento dos menus iterativos, barrando inputs inválidos ou nulos antes da montagem do JSON que será enviado ao servidor.

---
*Repositório desenvolvido exclusivamente para fins acadêmicos.*
