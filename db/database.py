import mysql.connector

class Accounts_db:
    def __init__(self,host, user, password, database):
        self.__host = host,
        self.__user = user,
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

    def execute_query(self, query):
        if self.__connection is not None:
            try:
                cursor = self.__connection.cursor()
                cursor.execute(query)
                self.__connection.commit()  # Se for uma query de alteração (INSERT, UPDATE, DELETE)
                return cursor.fetchall()    # Se for uma query de leitura (SELECT)
            except mysql.connector.Error as err:
                print(f"Erro ao executar a query: {err}")
                return None
            except Exception as e:
                print(f"Erro inesperado: {e}")
                return None
        else:
            print("Conexão ao banco de dados não estabelecida.")
            return None
    

