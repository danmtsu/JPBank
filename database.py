import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

class AccountsDB:
    def __init__(self, database='banks.db'):
        self.database = database
        self.connection = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.initialize_database()

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


    def initialize_database(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                cpf TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            )
            ''')
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                FOREIGN KEY (cpf) REFERENCES users(cpf)
            )
            ''')
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number INTEGER NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
            ''')
            self.connection.commit()
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
