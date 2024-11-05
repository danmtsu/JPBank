from bank import Bank
from view.interface import Interface
from tkinter import Tk
import threading
from threading import Lock, Semaphore
from concurrent.futures import ThreadPoolExecutor
import _mysql_connector
from database import Accounts_db
from user import User
from conta import Conta

class ControlBox:
    def __init__(self, root):
        self.__bank = Bank()
        self.__root = root
        self.__menu = Interface(self.__root)
        self.__user = None
        self.__conta = None
        self.__logado = False
        self.__database = None
        self.lock = Lock() #Mutex para proteger dados criticos


    def iniciar(self):
        try:
            self.__bank.connect_bank(host='localhost', user='root', password='root', database='banks')
            self.tela_inicial()

        except Exception as e:
            print("caiu aqui")
            print( f"Exception is :{e}")

    def tela_inicial(self):
        while not self.__logado:  # Enquanto não estiver logado
            decisao = self.__menu.menu_inicial()

            if decisao == 1:
                self.create_user()
            elif decisao == 2:
                self.process_login()
            elif decisao == 0:
                print("Saindo da aplicação...")
                break

    def process_login(self):
        info_login = self.__menu.menu_login()
        self.login_user(info_login[0], info_login[1])



    def create_user(self):
        user = self.__menu.menu_signup()
        if user:  # Verifica se o usuário clicou em cancelar
            self.__bank.createUser(user)
            print(f"Conta criada para {user['cpf']} com sucesso.")
            self.tela_usuario()

    
    def create_account(self,):
        self.__bank.createaccount(self.__user.cpf)



    def login_user(self, cpf, password):
        try:
            if cpf in self.__bank.users:
                if self.__bank.users[cpf].password == password:
                    self.__logado = True
                    self.__bank.get_user_accounts(cpf)
                    self.__menu.alerts("Login","Login realizado com sucesso!")
                    self.__user = self.__bank.users[cpf]
                    self.__menu.root.after(300,self.tela_selecao_conta,self.__user.contas) # Envia mensagem para a fila
                else:
                    self.__menu.errors("Login", "Senha incorreta")
            else:   
                self.__menu.errors("Login","CPF não encontrado")
        except Exception as e:
            self.__menu.errors("login",f"Erro ao realizar o login: {e}")


    def tela_usuario(self):
        self.__menu.clear_screen()  # Limpa a tela antes de mostrar a tela do usuário
        while self.__logado:  # Enquanto estiver logado
            decisao = self.__menu.menu_usuario()

            if decisao == 1:
                self.realiza_deposito()
            elif decisao == 2:
                self.realiza_saque()
            elif decisao == 3:
                self.realiza_transferencia()
            elif decisao == 4:
                self.verifica_extrato()
            elif decisao == 5:
                self.create_account()
            elif decisao == 6:
                self.change_accounts()
            elif decisao == 0:
                self.logout()

    def tela_selecao_conta(self,contas:list):
        """Abre uma tela com uma lista de contas para o usuário selecionar."""
        if contas:
            selected_account = int(self.__menu.menu_selecao_conta(contas))
            if selected_account:
                self.__conta = self.__bank.get_account_by_number(selected_account,self.__bank.contas,isList=False)
                print(self.__conta.numeroConta)
                self.tela_usuario()  # Acessa a tela de usuário com a conta selecionada
            else:
                print("Nenhuma conta selecionada.")
                self.tela_inicial
        else:
            print("usuario não possui nenhuma conta")


    def change_accounts(self,):
        """Abre uma tela com uma lista de contas para o usuário selecionar."""
        contas = self.__bank.get_user_accounts(self.__user.cpf)  # Obter as contas do usuário
        if contas:
            selected_account = self.__bank.contas[self.__menu.menu_selecao_conta(contas)]
            if selected_account:
                self.__conta = selected_account  # Define a conta selecionada
                self.tela_usuario()  # Acessa a tela de usuário com a conta selecionada
            else:
                print("Nenhuma conta selecionada.")

 
    def realiza_deposito(self):
        conta_valor = self.__menu.menu_deposito()
        if conta_valor:
            right_now = self.__bank.realiza_deposito(conta_valor)
            if right_now:
                self.__menu.root.after(300,self.__menu.alerts, "Depósito", f"Depósito no valor de {conta_valor[1]} deu boa!!")
            else:
                self.__menu.root.after(270, self.__menu.errors, "Depósito", f"Erro ao salvar o depósito")
                print("depósito está sendo processado")
        else:
            self.__menu.root.after(270, self.__menu.errors,"Depósito", f"Erro ao realizar o Depósito")



    def realiza_saque(self):
        valor = self.__menu.menu_saque()
        if valor:
            self.__bank.realiza_saque(self.__conta,valor)
            self.__menu.root.after(300,self.__menu.alerts,"Saque","Saque realizado com sucesso!!")
        else:
            self.__menu.root.after(270,self.__menu.errors,"Saque error", "erro ao realizar o saque")
   
    def realiza_transferencia(self):
        conta_valor = self.__menu.menu_transferencia()

        if conta_valor:
            numero_conta_destino, valor = conta_valor
            sucesso, mensagem = self.__bank.realiza_transacao(self.__conta, valor,numero_conta_destino)

            if sucesso:
                self.__menu.root.after(300, self.__menu.alerts, "Transferência", f"Transferência de {valor} realizada com sucesso!")
            else:
                self.__menu.root.after(270, self.__menu.errors, "Transferência", f"Erro ao realizar transferência: {mensagem}")
        else:
            self.__menu.root.after(270, self.__menu.errors, "Transferência", "Erro ao coletar dados para a transferência")


    def verifica_extrato(self):
        self.__menu.menu_extrato(self.__conta.transacoes, self.__conta.saldo)

    def logout(self):
        self.__logado = False
        self.__user = None
        self.__conta = None
        print("Você foi deslogado com sucesso.")
        self.__database.disconnect()
        self.tela_inicial()  # Retorna à tela inicial

