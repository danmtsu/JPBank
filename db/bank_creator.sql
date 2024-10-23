USE Bank;

-- Tabela User deve ser criada primeiro
CREATE TABLE User (
    cpf NUMERIC(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(12) NOT NULL,
    birthdate DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Accounts deve ser criada em segundo
CREATE TABLE Accounts (
    id SERIAL PRIMARY KEY,
    numero_conta NUMERIC(6) NOT NULL UNIQUE,
    agencia INT NOT NULL,
    saldo FLOAT NOT NULL DEFAULT 0.0,
    cpf NUMERIC(11) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cpf) REFERENCES User(cpf)
);

-- Tabela Transfers criada por último, após as outras duas
CREATE TABLE Transfers (
    id SERIAL PRIMARY KEY,
    conta_origem INT NOT NULL,
    conta_destino INT,
    tipo_transfer SMALLINT,
    valor FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conta_origem) REFERENCES Accounts(numero_conta),
    FOREIGN KEY (conta_destino) REFERENCES Accounts(numero_conta)
);
