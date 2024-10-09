from menu import Menu
from bank import Bank
from conta import Conta

class control_box:
    def __init__(self):
        self.__bank = Bank()
        self.__menu = Menu()
        self.__user = None
        self.__conta = None
        self.__logado = False
        
    @property
    def bank(self,):
        return self.__bank
    
    @property
    def conta(self,):
        return self.__conta
    
    @property
    def user(self):
        return self.__user
    
    @property
    def logado(self,):
        return self.__logado
    
    @logado.setter
    def logado(self,logado:bool):
        self.__logado = logado
    
    @user.setter
    def user(self,user):
        self.__user = user
    

    def tela_inicial(self,):
        decisao = self.__menu.menu_inical()
        if decisao == 1:
            user = self.__menu.menu_signup()
            self.__bank.criaConta(user)

        if decisao == 2:
            while self.__logado == False:
                info_login = self.__menu.menu_login()

                if f"{info_login[0]}" not in self.__bank.users or info_login[1] != self.bank.users[f"{info_login[0]}"].password:
                    print("CPF o ou senha incorreto")
                else:
                    self.__user = self.__bank.users[f"{info_login[0]}"]

                    self.__logado = True
        
        if self.__logado:
            self.tela_usuário()

    def tela_usuário(self,):
        while self.__logado == True:
            decisao = self.__menu.menu_usuario()
            if decisao == 1:
                conta_valor = self.__menu.menu_deposito()
                self.__bank.realiza_deposito(conta_valor[0],conta_valor[1])
                print(f"Depósito de {conta_valor[1]} Realizado para a conta {conta_valor[0]}")
            if decisao == 2:
                valor = self.__menu.menu_saque()
                self.__bank.realiza_saque(self.__user.accounts[0], valor)
                print(f"Saque de {valor} Realizado.")

            if decisao == 3:
                self.__bank.verifica_extrato(self.__user.accounts[0])

            if decisao == 0:
                self.__logado = False
                exit()
