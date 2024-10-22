from datetime import datetime
from conta import Conta

class User:
    def __init__(self, cpf, password:str, name:str, address:str, email:str, born:str):
        self.__cpf = cpf
        self.__name = name
        self.__address = address
        self.__email = email
        self.__born = born
        self.contas = []
        self.__password = password

    @property
    def cpf(self,):
        return self.__cpf
    
    @property
    def name(self,):
        return self.__name
    
    @property
    def password(self):
        return self.__password
    
    @property
    def email(self,):
        return self.__email
    
    @property
    def address(self,):
        return self.__address
    
    @property
    def born(self,):
        return self.__born
    
    
    def contas(self,):
        return self.contas
    
    @name.setter
    def name(self,name:str):
        self.__name = name

    @address.setter
    def address(self, address:str):
        self.__address = address

    @email.setter
    def email(self, email:str):
        self.__email = email

    
    def add_conta(self,conta:Conta):
        self.contas.append(conta)
        print(f"Conta de numero: {conta.numeroConta} e agencia: {conta.agencia} criada")

    
    def rm_conta(self,conta:Conta):
        self.contas.remove(conta)



    def __str__(self) -> str:
        return f"{self.__cpf} "
    