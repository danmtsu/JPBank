from menu import Menu
from bank import Bank
from conta import Conta

class control_box:
    def __init__(self):
        self.__bank = Bank()
        self.__menu = Menu()
        self.__user = None
        self.__conta = None
        
    @property
    def bank(self,):
        return self.__bank
    
    @property
    def conta(self,):
        return self.__conta
    
    @property
    def user(self):
        return self.__user
    
    @user.setter
    def user(self,user):
        self.__user = user
    

    def tela_inicial(self,):
        decisao = self.__menu.menu_inical()
        logado = False
        if decisao == 1:
            user = self.__menu.menu_signup()
            self.__bank.criaConta(user)

        if decisao == 2:
            while logado == False:
                info_login = self.__menu.menu_login()

                if f"{info_login[0]}" not in self.__bank.users or info_login[1] != self.bank.users[f"{info_login[0]}"].password:
                    print("CPF o ou senha incorreto")
                else:
                    self.__user = self.__bank.users[f"{info_login[0]}"]
                    logado = True
                    exit()

        