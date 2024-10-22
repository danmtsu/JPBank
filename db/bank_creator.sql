use Bank

CREATE TABLE IF NOT EXISTS Transfers(
    id SERIAL PRIMARY KEY,
    conta_origem INT NOT NULL,
    conta_estino INT,
    tipo_transfer SMALLINT,
    valor FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

)
CREATE TABLE IF NOT EXISTS accounts(
    id SERIAL PRIMARY KEY,
    numero NUMERIC(6) NOT NULL UNIQUE,
    agencia NOT NULL INT,
    saldo FLOAT NOT NULL DEFAULT 0.0,
    cpf NUMERIC(11) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cpf) REFERENCES User(cpf)
)

CREATE TABLE IF NOT EXISTS User(
    PRIMARY KEY cpf NUMERIC(11),
    nome varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(12) NOT NULL,
    birthdate DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)