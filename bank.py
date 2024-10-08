from conta import Conta
import random
from datetime import datetime
from user import User

class Bank():
    def __init__(self,):
        self.contas = []
        self.users = {}
        self.today = datetime.today().date()


    
    
    def is_same_day(self):
        if datetime.today().date() == self.today:
            return True
        else:
            self.today = datetime.today().date()
            return False
    
    def gerar_numero_agencia(self,):
        # Defina o intervalo para os números de agências que você deseja simular
        numero_minimo = 100000
        numero_maximo = 999999

        # Gere um número aleatório de agência dentro do intervalo definido
        numero_contas= random.randint(numero_minimo, numero_maximo)
        if numero_contas not in self.contas:
            self.contas.append(numero_contas)
        return numero_contas

    def criaConta(self, user:dict):
        if user["cpf"] != None and user["cpf"] not in self.contas:
            if user["name"] and user["born"] and user["address"] != None:
                usuario = User(user["cpf"],user["password"],user["name"],user["address"],user["email"],user["born"])
                conta = Conta(self.gerar_numero_agencia(), 1000)
                usuario.add_conta(conta.numeroConta)
                self.users[f"{user['cpf']}"] = usuario
                print(f"{self.users}")
                print("conta criada com sucesso")

        else:
            print("cpf já existente")

    def realiza_deposito(self,numeroConta:int,valor:float):
        if numeroConta > 0:
            contaEnvio = self.contas[f'{numeroConta}']
            contaEnvio.recebe_deposito(valor)
            contaEnvio.adiciona_transacao(f'{self.today}deposito de {valor}; Saldo: {contaEnvio.saldo}')
            return f"deposito de {valor} para a conta:{numeroConta}; Saldo atual de: {contaEnvio.saldo}"
        else:
            return "Valor de depósito inválido"
        

    def verifica_extrato(self,numeroConta:int):
        contaExtrato = self.contas[f"{numeroConta}"]
        return contaExtrato.transacoes
    
    def realiza_saque(self,numeroConta:int,valor:float):
            if f"{numeroConta}" in self.contas:
                contaSacada = self.contas[f"{numeroConta}"]
                if valor <= 500 and valor <= contaSacada.saldo and contaSacada.saqueHoje <3:
                    if self.is_same_day_day():
                        contaSacada.saqueHoje +=1
                    else:
                        contaSacada.saqueHoje = 0
                    contaSacada.realiza_saque(valor)
                    contaSacada.adiciona_transacao(f'{self.today} Saque realizado de {valor}; Saldo: {contaSacada.saldo}')
                    return f'Saque realizado de {valor}; Saldo: {contaSacada.saldo}'                   
                else:
                    print("valor de saque inválido")
            else:
                print(f"{numeroConta} inexistente.")