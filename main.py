from bank import Bank
from controller.control_box import ControlBox

def main():
    rodando = True
    controller = ControlBox()
    # Inicializa a conexão ao banco de dados
    #mysqlDB = Accounts_db(host="localhost", user="root", password="root", database="banks")
    #mysqlDB.connect()
    
    # Corrigindo a query SQL para criar a tabela
    #create_table_query = """
    #CREATE TABLE IF NOT EXISTS accounts (
    #    numero VARCHAR(255) NOT NULL UNIQUE,
    #    agencia INT NOT NULL,
    #    email VARCHAR(100) NOT NULL UNIQUE,
    #    nome VARCHAR(100) NOT NULL,
    #    saldo FLOAT NOT NULL DEFAULT 0.0,
    #    cpf VARCHAR(11) UNIQUE,
    #    nascimento DATE NOT NULL,
    #    PRIMARY KEY (numero, agencia)
    #)
    #"""
    #mysqlDB.execute_query(create_table_query)
    # Fecha a conexão com o banco
    #mysqlDB.disconnect()
    while rodando:
        controller.tela_inicial()
    # Inicializa o objeto Bank
    # Solicita o número da conta ao usuário
            # Exibe as contas criadas e a data formatada


# Executa a função principal
if __name__ == "__main__":
    main()
