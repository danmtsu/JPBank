from bank import Bank
from view.interface import Interface
from tkinter import Tk
import threading
from threading import Lock, Semaphore

class ControlBox:
    def __init__(self, root):
        self.__bank = Bank()
        self.__menu = Interface(root)
        self.__user = None
        self.__conta = None
        self.__logado = False
        self.lock = Lock() #Mutex para proteger dados criticos

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

    def iniciar(self):
        self.tela_inicial()

    def tela_inicial(self):
        while not self.__logado:  # Enquanto não estiver logado
            decisao = self.__menu.menu_inicial()

            if decisao == 1:
                self.create_user()
            elif decisao == 2:
                if self.login():  # Se o login for bem-sucedido
                    print("Login realizado com sucesso!")
                    self.tela_selecao_conta()  # Chama a tela do usuário
                else:
                    print("CPF ou senha incorretos. Tente novamente.")
            elif decisao == 0:
                print("Saindo da aplicação...")
                break

    def create_user(self):
        user = self.__menu.menu_signup()
        if user:  # Verifica se o usuário clicou em cancelar
            threading.Thread(target=self.__thread_create_user, args=(user, )).start()
            print(f"Conta criada para {user['cpf']} com sucesso.")

    def create_account(self,):
        self.__bank.createaccount(self.__user.cpf)
        self.tela_usuario()

    def login(self):
        info_login = self.__menu.menu_login()
        if info_login:  # Verifica se o usuário clicou em cancelar
            return self.login_user(info_login[0], info_login[1])
        return False  # Retorna False se o usuário cancelar

    def login_user(self, cpf, password):
        if cpf in self.__bank.users and self.__bank.users[cpf].password == password:
            self.__user = self.__bank.users[cpf]
            self.__conta = self.__user.contas[0]  # Acessa a primeira conta do usuário
            self.__logado = True
            return True
        return False

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

    def tela_selecao_conta(self):
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
            print("depósito está sendo processado")
            deposito_thread.start()
            print("Depósito realizado com sucesso.")

    def __thread_deposito(self,numero_conta,valor:float):
        with self.lock: #Garantir que o saldo seja acessado de forma segura
            self.__bank.realiza_deposito(numero_conta, valor)
            print("Depósito realizado com sucesso")

    def __thread_saque(self,numero_conta,valor:float):
        with self.lock:
            self.__bank.realiza_saque(numero_conta, valor)   
            
    def __thread_create_user(self,user):
        self.__bank.createUser(user)
        print("usuario criando")

    def realiza_saque(self):
        valor = self.__menu.menu_saque()
        if valor:
            thread_saque = threading.Thread(target=self.__thread_saque, args=(self.__conta, valor))
            print("Saque está sendo processado")
            thread_saque.start()

    def verifica_extrato(self):
        self.__menu.menu_extrato(self.__conta.transacoes, self.__conta.saldo)

    def logout(self):
        self.__logado = False
        self.__user = None
        self.__conta = None
        print("Você foi deslogado com sucesso.")

        # Retorna à tela inicial após logout
        self.tela_inicial()
