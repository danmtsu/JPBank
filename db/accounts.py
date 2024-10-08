class Accounts:
    def __init__(self, number:str, agencia:int, password:str, email:str, cpf:str):
        self.__numberAccount = number
        self.__agency = agencia
        self.__password = password
        self.__email = email
        self.__password = password
        self.__nascimento = None
        self.__nome = None
        self.saldo = 0
        self.__cpf = cpf


    def create_account(self,nascimento:str, nome:str):
        self.__nascimento = nascimento
        self.__nome = nome
        sqlScript = f"INSERT INTO accounts (numero, agencia, email, nome, saldo, cpf, nascimento, password) VALUES ({self.__numberAccount}, {self.__agency}, {self.__email},{self.__nome}, {self.saldo},{self.__cpf}, {self.__nascimento},{self.__password})"
        return sqlScript
    
    def delete_account(self, numberAccount, agency):
        sqlScript = f"DELETE FROM accounts WHERE numero = '{numberAccount}' AND agencia = '{agency}'"
        return sqlScript
    

