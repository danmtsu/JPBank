from conta import Conta
import random
from datetime import datetime

class Bank():
    def __init__(self,):
        self.__contas = {}
        self.__agencias = []
        self.today = datetime.today().date()


    
    @property
    def agencias(self):
        return self.__agencias
    
    @property
    def contas(self,):
        return self.__contas
    
    def is_same_day(self):
        if datetime.today().date() == self.today:
            return True
        else:
            self.today = datetime.today().date()
            return False
    
    def gerar_numero_agencia(self,):
        # Defina o intervalo para os números de agências que você deseja simular
        numero_minimo = 1000
        numero_maximo = 9999

        # Gere um número aleatório de agência dentro do intervalo definido
        numero_agencia = random.randint(numero_minimo, numero_maximo)
        if numero_agencia not in self.__agencias:
            self.__agencias.append(numero_agencia)
        return numero_agencia

    def criaConta(self, numero:int,agencia:int):
        if f"{numero}" not in self.__contas:
            if agencia in self.__agencias:
                self.__contas[f"{numero}"]= Conta(numero,agencia)
                print(self.__contas[f"{numero}"])
        else:
            print("numero de conta já existente")

    def realiza_deposito(self,numeroConta:int,valor:float):
        if numeroConta > 0:
            contaEnvio = self.__contas[f'{numeroConta}']
            contaEnvio.recebe_deposito(valor)
            contaEnvio.adiciona_transacao(f'{self.today}deposito de {valor}; Saldo: {contaEnvio.saldo}')
            return f"deposito de {valor} para a conta:{numeroConta}; Saldo atual de: {contaEnvio.saldo}"
        else:
            return "Valor de depósito inválido"
        

    def verifica_extrato(self,numeroConta:int):
        contaExtrato = self.__contas[f"{numeroConta}"]
        return contaExtrato.transacoes
    
    def realiza_saque(self,numeroConta:int,valor:float):
            if f"{numeroConta}" in self.__contas:
                contaSacada = self.__contas[f"{numeroConta}"]
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