import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

class AccountsDB:
    def __init__(self, database='./db/banks.db'):
        self.database = database
        self.connection = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def connect(self):
        if self.__connection is None:
            try:
                self.__connection = sqlite3.connect(self.database)
                logging.info("Conexão foi um sucesso")
            except sqlite3.Error as e:
                logging.error(f"Erro ao conectar ao banco de dados: {e}")

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None
            logging.info("Você foi desconectado!")

    def execute_query(self, query, params=None):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                connection.commit()
                return None


