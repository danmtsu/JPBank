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

    def change_accounts(self,):
        """Abre uma tela com uma lista de contas para o usuário selecionar."""
        contas = self.__bank.get_user_accounts(self.__user.cpf)  # Obter as contas do usuário
        if contas:
            selected_account = self.__bank.contas[self.__menu.menu_selecao_conta(contas)]
            if selected_account:
                self.__conta = selected_account  # Define a conta selecionada
            else:
                print("Nenhuma conta selecionada.")

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
        self.login(info_login[0], info_login[1])
        if self.__logado:  # Se o login for bem-sucedido
            self.tela_selecao_conta()
            print("Login realizado com sucesso!")
        else:
            print("CPF ou senha incorretos. Tente novamente.")


    def create_user(self):
        user = self.__menu.menu_signup()
        if user:  # Verifica se o usuário clicou em cancelar
            self.__bank.createUser(user)
            print(f"Conta criada para {user['cpf']} com sucesso.")
            self.tela_usuario()

    
    def create_account(self,):
        self.__bank.createaccount(self.__user.cpf)

    def login(self, cpf, password):
        if cpf and password:  # Verifica se o usuário clicou em cancelar
            self.login_user()
            

        return False  # Retorna False se o usuário cancelar

    def login_user(self, cpf, password):
        try:
            if cpf in self.__bank.users:
                if self.__bank.users[cpf].password == password:
                    self.__user = self.__bank.users[cpf]
                    self.__logado = True
                    self.__user.get_user_accounts(cpf)
                    self.__menu.alerts("Login","Login realizado com sucesso!")  # Envia mensagem para a fila
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
                self.verifica_extrato()
            elif decisao == 4:
                self.create_account()
            elif decisao == 5:
                self.change_accounts()
            elif decisao == 0:
                self.logout()

    def tela_selecao_conta(self,):
        contas = self.__user.contas
        """Abre uma tela com uma lista de contas para o usuário selecionar."""
        if contas:
            selected_account = self.__bank.contas[self.__menu.menu_selecao_conta(contas)]
            if selected_account:
                self.__conta = selected_account  # Define a conta selecionada
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
            deposito_thread = threading.Thread(target=self.__thread_deposito, args=(conta_valor[0], conta_valor[1]))
            deposito_thread.start()
            print("depósito está sendo processado")

    def __thread_deposito(self,numero_conta,valor:float):
        try:
            with self.lock:
                if str(numero_conta).strip() in self.__bank.contas:
                    if valor > 0:
                        self.__bank.realiza_deposito(numero_conta, valor)
                        self.__menu.root.after(270, self.__menu.alerts, "Depósito","Depósito realizado com sucesso!")
                    else:
                        self.__menu.root.after(270, self.__menu.errors,"Depósito","Depósito","Valor do depósito inválido")
                        print("Mensagem colocada na fila: Valor do depósito inválido")
                else:
                    self.__menu.root.after(270,self.__menu.errors,"Deposito","Conta de destino inexistente")
                    print("Mensagem colocada na fila: Conta de destino inexistente")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")


    def __thread_saque(self,valor:float):
        with self.lock:
            if self.__conta.saldo > valor and self.__conta.saqueHoje <3:

                self.__bank.realiza_saque(self.__conta, valor)

                self.__menu.root.after(270,self.__menu.alerts,"Saque",f"Saque realizado com sucesso!\n Seu saldo atual é de {self.__conta.saldo}")  # Envia mensagem para a fila
            else:
                self.__menu.root.after(180,"Saque", f"você tem saldo para essa transferencias:{valor} e saques realizados hoje?{self.__conta.saqueHoje}")




    def realiza_saque(self):
        valor = self.__menu.menu_saque()
        if valor:
            thread_saque = threading.Thread(target=self.__thread_saque, args=(valor, ))
            print("Saque está sendo processado")
            thread_saque.start()

    def verifica_extrato(self):
        self.__menu.menu_extrato(self.__conta.transacoes, self.__conta.saldo)

    def logout(self):
        self.__logado = False
        self.__user = None
        self.__conta = None
        print("Você foi deslogado com sucesso.")
        self.__database.disconnect()
        self.tela_inicial()  # Retorna à tela inicial

