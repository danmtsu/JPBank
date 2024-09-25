use accounts

CREATE TABLE IF NOT EXISTS accounts(
    numero VARCHAR(255) NOT NULL UNIQUE,
    agencia NOT NULL INT,
    email TEXT NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    saldo FLOAT NOT NULL DEFAULT 0.0,
    cpf VARCHAR(11) UNIQUE,
    nascimento DATE NOT NULL,
    PRIMARY KEY (numero,agencia)
)