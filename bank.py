from conta import Conta
import random
from datetime import datetime
from user import User
from database import Accounts_db
import threading
from threading import Lock, Event, Semaphore
from concurrent.futures import ThreadPoolExecutor

class Bank():
    def __init__(self,):
        self.contas = {}
        self.users = {}
        self.today = datetime.today().date()
        self.__database = None
        self.lock = Lock() #Mutex para proteger dados criticos
        self.event = Event()
        self.semaphore = Semaphore(1)
        self.executor = ThreadPoolExecutor(4)


    @property
    def database(self,):
        return self.__database
    
    @database.setter
    def database(self,host:str, user:str,password:str,database:str):
        self.__database = Accounts_db(host=host,user=user,password=password,database=database)

    # Configuração do banco e threads
    def connect_bank(self, host: str, database: str, password: str, user: str):
        self.__database = Accounts_db(host=host, database=database, password=password, user=user)
        self.__database.connect()
        
        # Inicia thread de usuários e de contas
        self.executor.submit(self.__thread_init_bank_user)
        self.executor.submit(self.__thread_init_bank_account)

        

    def createUser(self, user:dict = {}):
        if str(user["cpf"]) not in self.users and user["cpf"] and user["name"] and user["password"] and user["address"] and user["born"] is not None:
            usuario = User(user["cpf"],user["password"],user["name"],user["address"],user["email"],user["born"])
            self.users[str(usuario.cpf)] = usuario
            if isinstance(usuario, User):
                # Insere o novo usuário no banco de dados, usando query parametrizada
                insert_user_query = """
                    INSERT INTO User (cpf, nome, email, address, password, birthdate) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                print(user)
                user_params = (
                    int(usuario.cpf),  # CPF
                    usuario.name,      # Nome
                    usuario.email,     # Email
                    usuario.address,   # Endereço
                    usuario.password,  # Senha
                    usuario.born      # Data de nascimento
                )
                self.__database.execute_query(insert_user_query, user_params)
            self.createaccount(user["cpf"])

            return usuario

    def createaccount(self,cpf:str):
        condition = True
        user = self.users[cpf]
        while condition:
            numero_conta = str(random.randint(100000, 999999))
            if numero_conta not in self.contas:
                new_account = Conta(numero_conta, 1000)
                condition = False
        try:
            if isinstance(new_account, Conta):
                insert_account_query = """
                    INSERT INTO Accounts (numero_conta, agencia, saldo, cpf) 
                    VALUES (%s, %s, %s, %s)
                """
                account_params = (
                    int(new_account.numeroConta),  # Número da conta
                    int(new_account.agencia),      # Agência
                    float(new_account.saldo),      # Saldo
                    int(cpf)            # CPF do usuário (chave estrangeira)
                )
                self.__database.execute_query(insert_account_query, account_params)
                user.add_conta(new_account)
                self.contas[numero_conta] = new_account
                
            else:
                raise ValueError("Objeto passado não é uma instância de Conta.")
        except ValueError as e:
            print(f" Erro ao criar conta: {e}")
    
    def get_account_by_number(self,numero:int, contas:list):
        try:
            if len(contas) >0:
                numero = int(numero)
                for conta in contas:
                    if conta.numeroConta == numero:
                        return conta                        
            else:
                raise ValueError("Atributo contas está vazio")

        except ValueError as e:
            print(f"error na busca da conta: {e}")

    def get_user_accounts(self,cpf:str):
        cpf = int(cpf)
        user = self.users[f"{cpf}"]
        try:
            if len(user.contas) == 0:
                query = "SELECT numero_conta, agencia, saldo FROM Accounts WHERE cpf = %s"
                listaContas = self.__database.execute_query(query=query,params=(cpf, ))
                for conta in listaContas:
                    numero_conta = int(conta[0])
                    new_account = Conta(numero_conta,conta[1],conta[2])
                    user.add_conta(new_account)
                return user.contas
            else:
                return user.contas
        except ValueError as e:
            print(f"Erro ao mostrar a conta: {e}")

    def __thread_init_bank_user(self,):
        with self.lock:
            try:
                listaUsers = self.__database.execute_query("SELECT * FROM User")
                for user in listaUsers:
                    cpf = str(user[0])
                    self.users[cpf] = User(user[0], user[4], user[1], user[3], user[2], user[5])
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                self.event.set()  # Sinaliza a conclusão

    # Thread de inicialização de contas, aguardando o sinal da thread de usuários
    def __thread_init_bank_account(self,):
        self.event.wait()  # Aguarda sinal de conclusão de usuários
        with self.lock:
            try:
                listaAccounts = self.__database.execute_query("SELECT * FROM Accounts")
                for account in listaAccounts:
                    self.contas[f"{int(account[1])}"] = Conta(int(account[0]), account[2], account[3])
            except Exception as e:
                print(f"Exception is yes: {e}")
            finally:
                self.event.set()

    def realiza_deposito(self, numero_valor:tuple):
        try:

            # Inicia a thread corretamente
            self.executor.submit(self.__thread_realiza_deposito,int(numero_valor[0]), numero_valor[1])

        except Exception as e:
            print(f"Exception is: {e}")
            return False
        

    def verify_user(self, cpf, password):
        for user in self.users:
            if user['cpf'] == cpf and user['password'] == password:
                return True
        return False

    def verifica_extrato(self,transacoes:list):
        for i in transacoes:
            print(i)
    
    def realiza_saque(self,conta:Conta,valor:float):
        self.executor.submit(self.__thread_realiza_saque,conta.numeroConta, valor )


    def __thread_realiza_deposito(self,numero_conta:int, valor:float):
        with self.lock:
            self.semaphore.acquire()
            try:
                conta = self.contas[f"{numero_conta}"]
                conta.recebe_deposito(valor)

                query = "UPDATE Accounts SET saldo = %s WHERE numero_conta = %s"
                params = (conta.saldo, numero_conta)
                self.__database.execute_query(query=query, params=params)
            except Exception as e:
                print(f"Exception Depósito is: {e}")
                
            finally:
                print("Depósito finalizado com sucesso")
                self.semaphore.release()

    def __thread_realiza_saque(self,numero_conta:int, valor:float):
        with self.lock:
            self.semaphore.acquire()
            try:
                conta = self.contas[f"{numero_conta}"]
                if  valor <= 1200 and valor < conta.saldo:
                    conta.realiza_saque(valor)
                query = "UPDATE Accounts SET saldo = %s WHERE numero_conta = %s"
                params = (conta.saldo, numero_conta)
                self.__database.execute_query(query=query, params=params)
                
            except Exception as e:
                print(f"Exception saque is: {e}")
            
            finally:
                print("Saque realizado com sucesso")
                self.semaphore.release()
