from datetime import datetime

class Conta():
    def __init__(self,numero:int,agencia:int):
        self.__numeroConta = numero
        self.__agencia = agencia
        self.__saldo = 0
        self.__transacoes = []
        self.__saqueHoje = 0
        self.today = (datetime.today().date, datetime.today().time)
        
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
        self.transacoes.append(f"Depósito {self.today[0]} {self.today[1]} Valor de: {valor}")

    def realiza_saque(self,valor:float):
        self.__saldo -= valor
        self.saqueHoje +=1
        self.transacoes.append(f"Saque {self.today[0]} {self.today[1]} Valor de: {valor}")

    def __str__(self) -> str:
        return f"Conta: {self.__numeroConta} Agência: {self.__agencia}"