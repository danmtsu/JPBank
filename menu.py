class Menu:
    def __init__(self):
        self.__decision = int

    @property
    def decision(self):
        return self.__decision

    def menu_inical(self,):
        try:
            print("===> SELECIONE A OPÇÃO DESEJADA <===")
            print("aperte 1 para se tornar um cliente do banco")
            print("aperte 2 para acessar a sua conta no banco")
            print("aperte 0 para sair da aplicação")
            self.__decision = int(input("Qual a opção que você deseja?"))
            return self.__decision
        except ValueError:
            print("Por favor, digite um número válido.")
            return
        
    def menu_signup(self,):
   # Loop para criar contas até que o usuário digite 0
        while self.__decision != 0:
            if self.__decision == 1:
                password_correct = False
                cpf1 = int(input("por favor digitar o cpf do usuário: "))
                email1 = input("pot favor digitar o email do usuário: ")
                while password_correct != True:
                    password1 = input("por favor digite uma senha: ")
                    password2 = input("por favor digite novamente a senha: ")
                    if password1 == password2:
                        password_correct = True
                name1 = input("Por favor digite o nome do usuario: ")
                nascimento1 = input("Por favor digitar o dia de nascimento DD/MM/Y: ")
                endereco1 = input("por favor digite seu endereco: ")
                usuario = {"cpf": cpf1,"password":password1, "email":email1, "name":name1, "born":nascimento1, "address":endereco1}
                return usuario
            # Solicita o próximo número de conta

    def menu_usuario(self,):
        while self.__decision != 0:
            print("===> ESCOLHA A OPÇÃO DESEJADA <===")
            print(" Digite 1 para realizar um depósito ")
            print(" Digite 2 para realizar um saque ")
            print(" Digite 3 para visualizar o extrato ")
            self.__decision = int(input("Digite a opção desejada"))
            return self.__decision
        
    def menu_deposito(self,):
        print("==> escolha uma conta e o valor que deseja depositar <==")
        numerConta = input("Digite o numero da conta de destino: ")
        valor = float(input("Digite o valor do seu depósito: "))
        return (numerConta, valor)
    
    def menu_saque(self,):
        print("==> ESCOLHA O VALOR QUE DESEJA SACAR <==")
        valor = float(input("Digite o valor que deseja sacar:"))
        return valor
    
    def menu_extrato(self, transactions:list):
        print("===> EXTRATO DA CONTA <===")
        print(f"{transactions}")

    def menu_login(self,):
        cpf = int(input("Por favor digite seu CPF: "))
        password = input("Por favor digite sua senha: ")
        return (cpf, password)