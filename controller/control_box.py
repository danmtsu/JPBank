from bank import Bank
from controller.get_coins import GetCoins
from view.interface import Interface
from tkinter import Tk
import threading
from threading import Lock
from database import AccountsDB
from user import User
from conta import Conta

class ControlBox:
    def __init__(self, root):
        self.__database = AccountsDB(host='localhost', user='root', password='root', database='banks')
        self.__bank = Bank(database=self.__database)
        self.__root = root
        self.__menu = Interface(self.__root)
        self.__user = None
        self.__conta = None
        self.__logado = False
        self.__get_coins = GetCoins()
        self.__coins = {"Bitcoin": 0, "Dollar": 0}
        self.lock = Lock()  # Mutex para proteger dados críticos

    def iniciar(self):
        try:
            threading.Thread(target=self.__thread_init_coins, daemon=True).start()
            self.tela_inicial()
        except Exception as e:
            print("Erro ao iniciar aplicação:", e)

    def __thread_init_coins(self):
        with self.lock:
            try:
                self.__coins['Bitcoin'] = self.__get_coins.get_bitcoin_quote()
                self.__coins['Dollar'] = self.__get_coins.get_dollar_quote()
            except Exception as e:
                print(f"Erro ao obter cotação: {e}")

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
        user_data = self.__menu.menu_signup()
        if user_data:  # Verifica se o usuário clicou em cancelar
            try:
                self.__bank.create_user(user_data)
                print(f"Conta criada para {user_data['cpf']} com sucesso.")
                self.tela_usuario()
            except Exception as e:
                self.__menu.errors("Cadastro", f"Erro ao criar usuário: {e}")

    def create_account(self):
        try:
            self.__bank.create_account(self.__user.cpf)
            self.__menu.alerts("Conta", "Conta criada com sucesso!")
        except Exception as e:
            self.__menu.errors("Conta", f"Erro ao criar conta: {e}")

    def login_user(self, cpf, password):
        try:
            user = self.__bank.get_user(cpf, password)
            if user:
                self.__logado = True
                self.__user = user
                self.__menu.alerts("Login", "Login realizado com sucesso!")
                self.tela_selecao_conta(user.contas)
            else:
                self.__menu.errors("Login", "Credenciais inválidas.")
        except Exception as e:
            self.__menu.errors("Login", f"Erro ao realizar login: {e}")

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

    def tela_selecao_conta(self, contas):
        if contas:
            selected_account = int(self.__menu.menu_selecao_conta(contas))
            if selected_account:
                self.__conta = self.__bank.get_account_by_number(selected_account, self.__bank.contas, isList=False)
                self.tela_usuario()  # Acessa a tela de usuário com a conta selecionada
            else:
                self.__menu.errors("Conta", "Nenhuma conta selecionada.")
        else:
            self.__menu.errors("Conta", "Usuário não possui contas cadastradas.")

    def change_accounts(self):
        contas = self.__bank.get_user_accounts(self.__user.cpf)  # Obter as contas do usuário
        if contas:
            selected_account = int(self.__menu.menu_selecao_conta(contas))
            if selected_account:
                self.__conta = self.__bank.get_account_by_number(selected_account, self.__bank.contas, isList=False)
                self.tela_usuario()
            else:
                self.__menu.errors("Conta", "Nenhuma conta selecionada.")
        else:
            self.__menu.errors("Conta", "Usuário não possui contas cadastradas.")

    def realiza_deposito(self):
        with self.lock:
            conta_valor = self.__menu.menu_deposito()
            try:
                right_now = self.__bank.realiza_deposito(conta_valor)
                if right_now:
                    self.__menu.alerts("Depósito", f"Depósito de {conta_valor[1]} realizado com sucesso!")
                else:
                    self.__menu.errors("Depósito", "Erro ao realizar o depósito.")
            except Exception as e:
                self.__menu.errors("Depósito", f"Erro ao realizar o depósito: {e}")

    def realiza_saque(self):
        with self.lock:
            valor = self.__menu.menu_saque()
            try:
                self.__bank.realiza_saque(self.__conta, valor)
                self.__menu.alerts("Saque", "Saque realizado com sucesso!")
            except Exception as e:
                self.__menu.errors("Saque", f"Erro ao realizar saque: {e}")

    def realiza_transferencia(self):
        with self.lock:
            conta_valor = self.__menu.menu_transferencia()
            try:
                numero_conta_destino, valor = conta_valor
                sucesso, mensagem = self.__bank.run_transfer(self.__conta, valor, numero_conta_destino)

                if sucesso:
                    self.__menu.alerts("Transferência", f"Transferência de {valor} realizada com sucesso!")
                else:
                    self.__menu.errors("Transferência", f"Erro ao realizar transferência: {mensagem}")
            except Exception as e:
                self.__menu.errors("Transferência", f"Erro ao realizar transferência: {e}")

    def verifica_extrato(self):
        try:
            transactions = self.__bank.verifica_extrato(self.__conta.numeroConta)
            self.__menu.menu_extrato(transactions, self.__conta.saldo)
        except Exception as e:
            self.__menu.errors("Extrato", f"Erro ao carregar extrato: {e}")

    def logout(self):
        self.__logado = False
        self.__user = None
        self.__conta = None
        print("Você foi deslogado com sucesso.")
        self.__bank.disconnect()  # Certifique-se de que o método existe na classe Bank
        self.tela_inicial()
