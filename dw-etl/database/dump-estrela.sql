-- ------------------------------------------------------------------------------
-- 1. CRIAÇÃO DAS TABELAS DE DIMENSÃO 
-- ------------------------------------------------------------------------------

-- Dimensão Departamento

CREATE TABLE dim_departamento (
    sk_departamento SERIAL PRIMARY KEY,          -- Chave substituta (Data Warehouse)
    sigla VARCHAR(20),                           -- Chave original do CSV/Database
    nome VARCHAR(255) NOT NULL
);

-- Dimensão Professor

CREATE TABLE dim_professor (
    sk_professor SERIAL PRIMARY KEY,             -- Chave substituta (Data Warehouse)
    nome VARCHAR(255) NOT NULL,                 -- Chave original do CSV/Database
    tipo_jornada_trabalho VARCHAR(100),
    formacao VARCHAR(100),
    departamento_lotacao VARCHAR(255)            -- Texto com o nome do departamento 
);

-- Dimensão Disciplina (Componente Curricular)
-- Contém as matérias ofertadas.
CREATE TABLE dim_disciplina (
    sk_disciplina SERIAL PRIMARY KEY,            -- Chave substituta (Data Warehouse)
    nk_codigo_disciplina VARCHAR(50),            -- Código real da disciplina (ex: COMP0123)
    nome VARCHAR(255) NOT NULL,
    departamento_responsavel VARCHAR(255),
    cr_total INTEGER                             -- Número total de créditos
);

-- Dimensão Semestre

CREATE TABLE dim_semestre (
    sk_semestre SERIAL PRIMARY KEY,              -- Chave substituta (Data Warehouse)
    ano INTEGER NOT NULL,                        -- Ex: 2023, 2024
    periodo INTEGER NOT NULL,                    -- Ex: 1, 2
    
    -- Restrição para não cadastrar semestres duplicados
    CONSTRAINT uk_semestre UNIQUE (ano, periodo) 
);


-- ------------------------------------------------------------------------------
-- 2. CRIAÇÃO DA TABELA FATO 
-- ------------------------------------------------------------------------------

-- Fato Turmas
-- Associa as dimensões e armazena os fatos (métricas) daquela turma ocorrida.

CREATE TABLE fato_turmas (
    -- ID da Tabela Fato 
    id_fato_turma SERIAL PRIMARY KEY,
    
    -- Chaves Estrangeiras apontando para as Dimensões
    sk_professor INTEGER NOT NULL,
    sk_disciplina INTEGER NOT NULL,
    sk_departamento INTEGER NOT NULL,
    sk_semestre INTEGER NOT NULL,
    
    -- Chave natural para rastreio (código da turma no CSV/Database)
    nk_id_turma VARCHAR(50),
    
    -- Métricas / Fatos 
    qtd_discentes_matriculados INTEGER,
    media_notas NUMERIC(5,2),                    -- Usando NUMERIC para notas (ex: 8.75)
    qtd_aprovados INTEGER,                       -- Nota >= 5
    qtd_reprovados INTEGER,                      -- Nota < 5
    
    -- Restrições 
    CONSTRAINT fk_fato_professor FOREIGN KEY (sk_professor) REFERENCES dim_professor (sk_professor),
    CONSTRAINT fk_fato_disciplina FOREIGN KEY (sk_disciplina) REFERENCES dim_disciplina (sk_disciplina),
    CONSTRAINT fk_fato_departamento FOREIGN KEY (sk_departamento) REFERENCES dim_departamento (sk_departamento),
    CONSTRAINT fk_fato_semestre FOREIGN KEY (sk_semestre) REFERENCES dim_semestre (sk_semestre)
);


