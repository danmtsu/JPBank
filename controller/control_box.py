from bank import Bank
from view.interface import Interface

class ControlBox:
    def __init__(self, root):
        self.__bank = Bank()
        self.__menu = Interface(root)
        self.__user = None
        self.__conta = None
        self.__logado = False

    def iniciar(self):
        self.tela_inicial()

    def tela_inicial(self):
        while not self.__logado:  # Enquanto não estiver logado
            decisao = self.__menu.menu_inicial()

            if decisao == 1:
                self.criar_conta()
            elif decisao == 2:
                if self.login():  # Se o login for bem-sucedido
                    print("Login realizado com sucesso!")
                    self.tela_usuario()  # Chama a tela do usuário
                else:
                    print("CPF ou senha incorretos. Tente novamente.")
            elif decisao == 0:
                print("Saindo da aplicação...")
                break

    def criar_conta(self):
        user = self.__menu.menu_signup()
        if user:  # Verifica se o usuário clicou em cancelar
            self.__bank.criaConta(user)
            print(f"Conta criada para {user['cpf']} com sucesso.")

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
            elif decisao == 0:
                self.logout()

    def realiza_deposito(self):
        conta_valor = self.__menu.menu_deposito()
        if conta_valor:
            self.__bank.realiza_deposito(conta_valor[0], conta_valor[1])
            print("Depósito realizado com sucesso.")

    def realiza_saque(self):
        valor = self.__menu.menu_saque()
        if valor:
            self.__bank.realiza_saque(self.__conta, valor)
            print("Saque realizado com sucesso.")

    def verifica_extrato(self):
        self.__menu.menu_extrato(self.__conta.transacoes)

    def logout(self):
        self.__logado = False
        self.__user = None
        self.__conta = None
        print("Você foi deslogado com sucesso.")

        # Retorna à tela inicial após logout
        self.tela_inicial()
