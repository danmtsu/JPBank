from conta import Conta
import random
from datetime import datetime
from user import User

class Bank():
    def __init__(self,):
        self.contas = {}
        self.users = {}
        self.today = datetime.today().date()


    def criaConta(self, user:dict):
        n = 0
        if user["cpf"] != None and user["cpf"] not in self.contas:
            if user["name"] and user["born"] and user["address"] != None:
                usuario = User(user["cpf"],user["password"],user["name"],user["address"],user["email"],user["born"])
                while n < 1:
                    numero_conta = random.randint(100000, 999999)
                    if numero_conta not in self.contas:
                        self.contas[f"{numero_conta}"] = Conta(numero_conta,1000)
                        n = 1
                usuario.add_conta(f"{numero_conta}")
                self.users[f"{user['cpf']}"] = usuario
                print(f"{self.users}")
                print("conta criada com sucesso")

        else:
            print("cpf já existente")

    def realiza_deposito(self,numeroConta:str,valor:float):
        if numeroConta in self.contas:
            self.contas[numeroConta].recebe_deposito(valor)     
            return f"deposito de {valor} para a conta:{numeroConta};"
        else:
            return "Valor de depósito inválido"
        

    def verifica_extrato(self,numeroConta):
        contaExtrato = self.contas[f"{numeroConta}"]
        return contaExtrato.transacoes
    
    def realiza_saque(self,numeroConta:str,valor:float):
            if numeroConta in self.contas:
                contaSacada = self.contas[numeroConta]
                if valor <= 500 and valor <= contaSacada.saldo and contaSacada.saqueHoje <3:
                    contaSacada.realiza_saque(valor)
                    contaSacada.adiciona_transacao(f'{self.today} Saque realizado de {valor}; Saldo: {contaSacada.saldo}')
                    return f'Saque realizado de {valor}; Saldo: {contaSacada.saldo}'                   
                else:
                    print("valor de saque inválido")
            else:
                print(f"{numeroConta} inexistente.")