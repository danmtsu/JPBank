from datetime import datetime

class Conta():
    def __init__(self,numero:str,agencia:int,saldo:float = 0):
        self.__numeroConta = numero
        self.__agencia = agencia
        self.__saldo = saldo
        self.__transacoes = []
        self.__saqueHoje = 0
        self.today = (datetime.today().date(), datetime.today().time())
        
    @property
    def transacoes(self,):
        return self.__transacoes

    @property
    def numeroConta(self):
        return self.__numeroConta
    
    @property
    def agencia(self,):
        return self.__agencia
    
    @property
    def saldo(self,):
        return self.__saldo
    
    @saldo.setter
    def saldo(self,valor:float):
        self.__saldo = valor
    
    @property
    def saqueHoje(self,):
        return self.__saqueHoje

    def recebe_deposito(self,valor:float):
        self.__saldo +=valor
        print(f"deposito recebido seu saldo atual é de : {self.__saldo}")
        now = datetime.now()
        data_formatada = now.strftime("%Y-%m-%d %H:%M:%S")  # Formatação com segundos
        self.transacoes.append(f"Depósito {data_formatada} Valor de: {valor}")

    def realiza_saque(self,valor:float):
        self.__saldo -= valor
        self.__saqueHoje +=1
        print(f"Saque realizado, seu saldo atual é de:{self.__saldo}")
        now = datetime.now()
        data_formatada = now.strftime("%Y-%m-%d %H:%M:%S")  # Formatação com segundos
        self.transacoes.append(f"Saque {data_formatada} Valor de: {valor}")

    def __str__(self) -> str:
        return f"Conta: {self.__numeroConta} Agência: {self.__agencia}"