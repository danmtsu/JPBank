from menu import Menu
from bank import Bank

class ControlBox:
    def __init__(self):
        self.__bank = Bank()
        self.__menu = Menu()
        self.__user = None
        self.__conta = None
        self.__logado = False

    @property
    def bank(self):
        return self.__bank

    @property
    def conta(self):
        return self.__conta

    @property
    def user(self):
        return self.__user

    @property
    def logado(self):
        return self.__logado

    @logado.setter
    def logado(self, logado: bool):
        self.__logado = logado

    @user.setter
    def user(self, user):
        self.__user = user

    def tela_inicial(self):
        decisao = self.__menu.menu_inical()
        if decisao == 1:
            # Criação de conta
            user = self.__menu.menu_signup()
            self.__bank.criaConta(user)

        elif decisao == 2:
            # Processo de login
            while not self.__logado:
                info_login = self.__menu.menu_login()

                # Verifica se o CPF existe nos usuários e a senha está correta
                if f"{info_login[0]}" in self.__bank.users and info_login[1] == self.__bank.users[f"{info_login[0]}"].password:
                    # Login bem-sucedido
                    self.__user = self.__bank.users[f"{info_login[0]}"]
                    self.__conta = self.__user.contas[0]  # Acessa a primeira conta do usuário
                    self.__logado = True
                    print("Login realizado com sucesso!")
                else:
                    print("CPF ou senha incorretos. Tente novamente.")

        if self.__logado:
            self.tela_usuario()

    def tela_usuario(self):
        while self.__logado:
            decisao = self.__menu.menu_usuario()

            if decisao == 1:
                # Depósito
                conta_valor = self.__menu.menu_deposito()
                self.__bank.realiza_deposito(conta_valor[0], conta_valor[1])
                print(f"Depósito de {conta_valor[1]} realizado para a conta {conta_valor[0]}")

            elif decisao == 2:
                # Saque
                valor = self.__menu.menu_saque()
                resultado = self.__bank.realiza_saque(self.__conta, valor)
                print(resultado)

            elif decisao == 3:
                # Verifica extrato
                #extrato = self.__bank.verifica_extrato(self.__conta.numeroConta)
                self.__menu.menu_extrato(self.__conta.transacoes)
                print(f"seu saldo atual é de:{self.__conta.saldo}")

            elif decisao == 0:
                # Logout
                self.__logado = False
                print("Logout realizado com sucesso.")
                break
