USE banks;

-- Tabela Users deve ser criada primeiro
CREATE TABLE Users (
    cpf VARCHAR(11) PRIMARY KEY, -- Alterado para VARCHAR para manter zeros à esquerda
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL, -- Senha como hash
    birthdate DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Accounts deve ser criada em segundo
CREATE TABLE Accounts (
    numero_conta INT NOT NULL UNIQUE, -- Alterado para INT para consistência com Transfers
    agencia INT NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Alterado para DECIMAL para precisão monetária
    cpf VARCHAR(11) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cpf) REFERENCES Users(cpf)
);

-- Tabela Transfers criada por último
CREATE TABLE Transfers (
    id SERIAL PRIMARY KEY, -- Campo `id` mantido para auditoria e buscas eficientes
    conta_origem INT NOT NULL,
    conta_destino INT,
    tipo_transfer SMALLINT NOT NULL, -- Adicionado NOT NULL
    valor DECIMAL(10, 2) NOT NULL, -- Alterado para DECIMAL para precisão monetária
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conta_origem) REFERENCES Accounts(numero_conta),
    FOREIGN KEY (conta_destino) REFERENCES Accounts(numero_conta)
);

