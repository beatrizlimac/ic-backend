-- 3. Teste de Banco de Dados
CREATE DATABASE IF NOT EXISTS ans_data;
USE ans_data;

-- Criar tabela para os dados contábeis das operadoras
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id_demonstracoes INT AUTO_INCREMENT PRIMARY KEY,
    data_demonstracao DATE,
    registro_ans INT,
    cd_conta_contabil INT,
    descricao VARCHAR(300),
    vl_saldo_inicial VARCHAR(255),
    vl_saldo_final VARCHAR(255),
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela para os dados cadastrais das operadoras
CREATE TABLE IF NOT EXISTS operadoras_ativas (
    id_operadoras INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20),
    cnpj VARCHAR(20),
    razao_social VARCHAR(355),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(15),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(5),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(25),
    fax VARCHAR(15),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(255),
    regiao_da_comercializacao VARCHAR(10),
    data_registro_ans DATE,
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

LOAD DATA INFILE '/1T2023.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/2T2023.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/3T2023.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/4T2023.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/1T2024.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/2T2024.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/3T2024.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/4T2024.csv' 
INTO TABLE demonstracoes_contabeis 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(data_demonstracao, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)

LOAD DATA INFILE '/docker-entrypoint-initdb.d/Relatorio_cadop' 
INTO TABLE operadoras_ativas 
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_da_comercializacao, data_registro_ans);


-- 3.5 Consultas Analíticas
-- 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre
SELECT 
    op.cnpj AS cnpj_operadora,
    op.razao_social AS razao_social,
    dc.descricao AS categoria,
    SUM(REPLACE(NULLIF(dc.vl_saldo_final, ''), ',', '.')) AS total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras_ativas op ON op.registro_ans = dc.registro_ans
WHERE dc.descricao LIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
  AND dc.data_demonstracao BETWEEN '2024-10-01' AND '2024-12-31'
GROUP BY op.cnpj, op.razao_social, dc.descricao
ORDER BY total_despesas DESC
LIMIT 10;

-- 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último ano
SELECT 
    op.cnpj AS cnpj_operadora,
    op.razao_social AS razao_social,
    dc.descricao AS categoria,
    SUM(REPLACE(NULLIF(dc.vl_saldo_final, ''), ',', '.')) AS total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras_ativas op ON op.registro_ans = dc.registro_ans
WHERE dc.descricao LIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
  AND YEAR(dc.data_demonstracao) = 2024
GROUP BY op.cnpj, op.razao_social, dc.descricao
ORDER BY total_despesas DESC
LIMIT 10;