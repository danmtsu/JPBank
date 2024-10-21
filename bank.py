from conta import Conta
import random
from datetime import datetime
from user import User

class Bank():
    def __init__(self,):
        self.contas = {}
        self.users = {}
        self.today = datetime.today().date()

    def createUser(self, user:dict = {}):
        n = 0
        if user["cpf"] != None and user["cpf"] not in self.users:
            if user["name"] and user["born"] and user["address"] != None:
                usuario = User(user["cpf"],user["password"],user["name"],user["address"],user["email"],user["born"])
                self.users[f"{user['cpf']}"] = usuario
                self.createaccount(user["cpf"])

        else:
            print("cpf já existente")

    def createaccount(self,cpf:str):
        condition = True
        user = self.users[cpf]
        while condition:
            numero_conta = str(random.randint(100000, 999999))
            if numero_conta not in self.contas:
                new_account = Conta(numero_conta, 1000)
                condition = False
        try:
            if isinstance(new_account, Conta):
                user.add_conta(new_account)
                self.contas[numero_conta] = new_account
                
            else:
                raise ValueError("Objeto passado não é uma instância de Conta.")
        except ValueError as e:
            print(f" Erro ao criar conta: {e}")

    def get_user_accounts(self,cpf:str):
        user = self.users[cpf]
        try:
            return user.contas
        except ValueError as e:
            print(f"Erro ao mostrar a conta: {e}")

    def realiza_deposito(self, numeroConta: str, valor: float):
        conta = self.contas[numeroConta]
        conta.recebe_deposito(valor)
        return f"Depósito de {valor} realizado com sucesso na conta {numeroConta}."


    def verify_user(self, cpf, password):
        for user in self.users:
            if user['cpf'] == cpf and user['password'] == password:
                return True
        return False

    def verifica_extrato(self,transacoes:list):
        for i in transacoes:
            print(i)
    
    def realiza_saque(self,conta:Conta,valor:float):
        if conta.saqueHoje <3:
            if  valor <= 500 and valor <= conta.saldo:
                conta.realiza_saque(valor)
                print(f'{self.today} Saque realizado de {valor}; Saldo: {conta.saldo}')
                return f'Saque realizado de {valor}; Saldo: {conta.saldo}'                   
        else:
            print("limite de saque excedido")

    