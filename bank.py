from conta import Conta
import random
from datetime import datetime
from user import User
from database import AccountsDB
import threading
from threading import Lock, Event, Semaphore
from concurrent.futures import ThreadPoolExecutor
import queue
import time

class Bank():
    def __init__(self,):
        self.contas = {}
        self.users = {}
        self.today = datetime.today().date()
        self.__database = AccountsDB(database='./db/banks.db')
        self.lock = Lock() #Mutex para proteger dados criticos
        self.event = Event()
        self.semaphore = Semaphore(1)
        self.executor = ThreadPoolExecutor(2)
        self.fila_transacoes = queue.Queue()
        self.thread_transacoes = threading.Thread(target=self.__processa_fila_transacoes, daemon=True)
        self.thread_transacoes.start() 


    @property
    def database(self,):
        return self.__database
    
    @database.setter
    def database(self,host:str, user:str,password:str,database:str):
        self.__database = AccountsDB(host=host,user=user,password=password,database=database)

    # Configuração do banco e threads
    def connect_bank(self, database: str='./db/banks.db'):
        self.__database = AccountsDB(database=database)
        self.__database.connect()
    
        
        # Inicia thread de usuários e de contas
        self.executor.submit(self.__thread_init_bank_user)
        self.executor.submit(self.__thread_init_bank_account)

        
    def disconnect_bank(self):
        if self.__database:
            self.__database.close()


    def createUser(self, user: dict = {}):
        try:
            if all(user.get(key) for key in ["cpf", "name", "password", "address", "born", "email"]):
                # Assume o formato da data já como 'YYYY-MM-DD'
                born_date = user["born"]

                usuario = User(
                    user["cpf"], user["password"], user["name"], 
                    user["address"], user["email"], born_date
                )

                # Query para inserir no banco
                insert_user_query = """
                INSERT INTO Users (cpf, nome, email, address, hashed_password, birthdate) 
                VALUES (?, ?, ?, ?, ?, ?)
                """
                user_params = (
                    usuario.cpf, usuario.name, usuario.email, 
                    usuario.address, usuario.password, usuario.born
                )

                # Insere no banco
                self.__database.execute_query(insert_user_query, user_params)

                # Cria conta associada ao usuário
                self.createAccount(user["cpf"])
                return usuario
            else:
                print("Erro: Dados do usuário estão incompletos.")
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")


    def createAccount(self,cpf:str):
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
                VALUES (?, ?, ?, ?)
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
    
    def get_account_by_number(self,numero:int, contas,isList:bool = True):
        try:
            if isList:
                if len(contas) >0:
                    numero = int(numero)
                    for conta in contas:
                        if conta.numeroConta == numero:
                            return conta                        
                else:
                    raise ValueError("Atributo contas está vazio")
            else:
                if str(numero) in contas:
                    return contas[f"{numero}"]
                else:
                    raise ValueError("Numero de conta inválido")
                    

        except ValueError as e:
            print(f"error na busca da conta: {e}")

    def get_user_accounts(self,cpf:str):
        cpf = int(cpf)
        user = self.users[f"{cpf}"]
        try:
            if len(user.contas) == 0:
                query = "SELECT numero_conta, agencia, saldo FROM Accounts WHERE cpf = ?"
                listaContas = self.__database.execute_query(query=query, params=(str(cpf), ))

                for conta in listaContas:
                    numero_conta = int(conta[0])
                    new_account = Conta(numero_conta,conta[1],conta[2])
                    user.add_conta(new_account)
                return user.contas
            else:
                return user.contas
        except ValueError as e:
            print(f"Erro ao mostrar a conta: {e}")

    def __processa_fila_transacoes(self):
            while True:
                # Bloqueia até que haja uma nova transação na fila
                transacao = self.fila_transacoes.get()  # Bloqueia até ter uma transação

                # Extrai os dados da transação
                tipo = transacao['tipo']
                conta_origem = transacao['conta_origem']
                conta_destino = transacao['conta_destino']
                valor = transacao['valor']

                try:
                    # Insere a transação na tabela Transfers
                    query = """
                        INSERT INTO Transfers (conta_origem, conta_destino, tipo_transfer, valor, created_at)
                        VALUES (%s, %s, %s, %s, NOW())
                    """
                    tipo_transfer = 1 if tipo == 'deposito' else 2  # Define o tipo de transferência

                    # Executa a inserção na tabela
                    self.__database.execute_query(query, (conta_origem, conta_destino, tipo_transfer, valor))

                except Exception as e:
                    print(f"Erro ao registrar transação na tabela Transfers: {e}")

                finally:
                    # Marca a tarefa como concluída para a fila
                    self.fila_transacoes.task_done()

    def __thread_init_bank_user(self,):
        with self.lock:
            try:
                listaUsers = self.__database.execute_query("SELECT * FROM Users")
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
                    self.contas[f"{int(account[1])}"] = Conta(int(account[1]), account[2], account[3])
            except Exception as e:
                print(f"Exception is yes: {e}")
            finally:
                self.event.set()
                
    def __thread_get_account_transfers(self,Account:Conta):
        with self.lock:
            try:
                listaTransfers = self.__database.execute_query(f"SELECT * FROM Transfers WHERE conta_origem = {Account.numeroConta}")
                for transfer in listaTransfers:
                    Account.add_transactions(transfer)
            except Exception as e:
                print('{e}')
            finally:
                self.event.set()

    def realiza_deposito(self, numero_valor:tuple):
        try:

            # Inicia a thread corretamente
            self.executor.submit(self.__thread_realiza_deposito,int(numero_valor[0]), numero_valor[1])
            return True
        except Exception as e:
            print(f"Exception is: {e}")
            return False
        

    def verify_user(self, cpf, password):
        for user in self.users:
            if user['cpf'] == cpf and user['password'] == password:
                return True
        return False

    def verifica_extrato(self, numero_conta):
        try:
            conta = self.contas.get(str(numero_conta))
            if conta:
                self.executor.submit(self.__thread_get_account_transfers, conta)
                return conta.transacoes
            else:
                print("Conta não encontrada.")
                return []
        except Exception as e:
            print(f"Erro ao consultar o extrato: {e}")
            return []
    
    def formatar_extrato(self, transacoes,numero_conta):
        if not transacoes:
            return "Nenhuma transação encontrada."

        extrato_formatado = "Extrato da Conta:\n"
        for transacao in transacoes:
            origem, destino, tipo, valor, data = transacao
            if origem == destino:
                operacao = "Depósito" if tipo == 1 else "Saque"
            else:
                operacao = "Transferência Enviada" if origem == numero_conta else "Transferência Recebida"

            extrato_formatado += f"{data} - {operacao} - Valor: R${valor:.2f} - Destino: {destino if operacao == 'Transferência Enviada' else origem}\n"
        return extrato_formatado

    
    def realiza_saque(self,conta:Conta,valor:float):
        try:
            self.executor.submit(self.__thread_realiza_saque,conta.numeroConta, valor )
        except Exception as e:
            print(f"Exception is: {e}")
            return False
        
    def run_transfer(self, conta: Conta, valor: float, contaDestino: int):
        print(contaDestino)
        print(conta.saldo)
        if str(contaDestino) not in self.contas:
            return False, "Conta de destino não encontrada."

        # Valida a operação na conta origem e destino
        if valor <= conta.saldo:
            conta.realiza_transferencia(valor)

            conta_destino_obj = self.contas[str(contaDestino)]
            print(conta)
            print(conta_destino_obj)
            conta_destino_obj.recebe_transferencia(valor)
        else:
            return False, "Saldo insuficiente para a transferencia"
        # Envia a tarefa para o executor
        self.executor.submit(self.__thread_realiza_transacao, conta, valor, conta_destino_obj) 
        return True, "Transferencia sendo processada."

    def __thread_realiza_transacao(self, contaOrigem: Conta, valor: float, contaDestino: Conta):
        with self.lock:
            try:
                print("chegou aqui")
                # Executa a transação como um bloco atômico
                queries = [
                    ("UPDATE Accounts SET saldo = %s WHERE numero_conta = %s", (contaOrigem.saldo, contaOrigem.numeroConta)),
                    ("UPDATE Accounts SET saldo = %s WHERE numero_conta = %s", (contaDestino.saldo, contaDestino.numeroConta)),
                    ("INSERT INTO Transfers (conta_origem, conta_destino, tipo_transfer, valor) VALUES (%s, %s, 3, %s)",
                     (contaOrigem.numeroConta, contaDestino.numeroConta, valor))
                ]

                # Executa cada query
                for query, params in queries:
                    self.__database.execute_query(query, params)
                    print("executou aqui")


            except Exception as e:
                print(f"Erro na transferência: {e}")


    def __thread_realiza_deposito(self,numero_conta:int, valor:float):
        with self.lock:
            self.semaphore.acquire()
            try:
                conta = self.contas[f"{numero_conta}"]
                conta.recebe_deposito(valor)

                query = "UPDATE Accounts SET saldo = %s WHERE numero_conta = %s"
                params = (conta.saldo, numero_conta)
                self.__database.execute_query(query=query, params=params)
                add_transfer = "INSERT INTO Transfers (conta_origem, conta_destino, tipo_transfer, valor) VALUES (%s, %s, %s, %s)"
                params_transfer = ( numero_conta, None, 1,  valor)
                self.__database.execute_query(query=add_transfer,params=params_transfer)
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
                add_transfer = "INSERT INTO Transfers (conta_origem, conta_destino, tipo_transfer, valor) VALUES (%s, %s, %s, %s)"
                params_transfer = (numero_conta,None, 2,valor)
                self.__database.execute_query(query=add_transfer,params=params_transfer)

                
            except Exception as e:
                print(f"Exception saque is: {e}")
            
            finally:
                print("Saque realizado com sucesso")
                self.semaphore.release()
