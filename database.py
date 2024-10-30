import mysql.connector

class Accounts_db:
    def __init__(self, host, user, password, database):
        self.__host = host  # sem vírgula
        self.__user = user  # sem vírgula
        self.__password = password
        self.__database = database
        self.__connection = None


    def connect(self):
        if self.__connection == None:
            try:
                self.__connection = mysql.connector.connect(
                    host=self.__host,
                    user=self.__user,
                    password=self.__password,
                    database=self.__database
                )
                print("Conexão foi um sucesso")
            except Exception as e:
                print(f"Erro ao connectar ao banco de dados:{e}")

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None
            print("Você foi desconectado!")

        
    def execute_query(self, query, params=None):
        """
        Executa uma query no banco de dados. Se for uma leitura (SELECT), retorna os resultados.
        Se for uma alteração (INSERT, UPDATE, DELETE), realiza o commit automaticamente.

        Args:
            query (str): A query SQL a ser executada.
            params (tuple): Os parâmetros para a query, caso seja uma query parametrizada.

        Returns:
            list: Resultados da consulta SELECT ou None para outras operações.
        """
        if self.__connection is not None:
            try:
                cursor = self.__connection.cursor()

                # Se houver parâmetros, use-os, senão execute a query diretamente
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Commit para operações de modificação de dados
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    self.__connection.commit()
                    return None

            except mysql.connector.Error as err:
                str = f"Erro ao executar a query: {err}"
                return str
        else:
            str = "Conexão ao banco de dados não estabelecida."
            return str


