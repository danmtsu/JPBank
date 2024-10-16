from conta import Conta
import random
from datetime import datetime
from user import User

class Bank():
    def __init__(self,):
        self.contas = {}
        self.users = {}
        self.today = datetime.today().date()


    def criaConta(self, user:dict = {}):
        n = 0
        if user["cpf"] != None and user["cpf"] not in self.contas:
            if user["name"] and user["born"] and user["address"] != None:
                usuario = User(user["cpf"],user["password"],user["name"],user["address"],user["email"],user["born"])
                while n < 1:
                    numero_conta = str(random.randint(100000, 999999))
                    if numero_conta not in self.contas:
                        new_account = Conta(numero_conta,1000)
                        self.contas[numero_conta] = new_account
                        n = 1
                usuario.add_conta(new_account)
                self.users[f"{user['cpf']}"] = usuario
                print("conta criada com sucesso")

        else:
            print("cpf já existente")

    def realiza_deposito(self,numeroConta:str,valor:float):
        if int(valor) <= 0:
             print("Valor de depósito inválido")
             return
        if numeroConta in self.contas:
            conta = self.contas[numeroConta]
            conta.recebe_deposito(valor)     
            return f"deposito de {valor} para a conta:{numeroConta};"
        else:
            return f"Digite uma conta existente"

    def verify_user(self, cpf, password):
        for user in self.users:
            if user['cpf'] == cpf and user['password'] == password:
                return True
        return False

    def verifica_extrato(self,transacoes:list):
        for i in transacoes:
            print(i)
    
    def realiza_saque(self,conta:Conta,valor:float):
        if valor <= 0:
            print( "valor de saque inválido")
            return
        if conta.numeroConta in self.contas:
            if conta.saqueHoje <3:
                if  valor <= 500 and valor <= conta.saldo:
                    conta.realiza_saque(valor)
                    print(f'{self.today} Saque realizado de {valor}; Saldo: {conta.saldo}')
                    return f'Saque realizado de {valor}; Saldo: {conta.saldo}'                   
            else:
                print("limite de saque excedido")
        else:
            print(f"{conta.numeroConta} inexistente.")
    