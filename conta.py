class Conta():
    def __init__(self,numero:int,agencia:int):
        self.__numeroConta = numero
        self.__agencia = agencia
        self.saldo = 0
        self.__transacoes = []
        self.saqueHoje = 0

    @property
    def transacoes(self,):
        return self.__transacoes

    @property
    def numeroConta(self):
        return self.__numeroConta
    
    @property
    def agencia(self,):
        return self.__agencia
    

    def recebe_deposito(self,valor:float):
        self.saldo +=valor

    def realiza_saque(self,valor:float):
        self.saldo -= valor

    def adiciona_transacao(self,transacao):
        self.transacoes.append(transacao)

    def __str__(self) -> str:
        return f"Conta: {self.__numeroConta} Agência: {self.__agencia}"