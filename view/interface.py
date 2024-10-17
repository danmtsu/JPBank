import tkinter as tk
from tkinter import simpledialog, messagebox

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("JPBank - Sistema Bancário")
        self.root.geometry("400x300")
        self.__decision = None

    @property
    def decision(self):
        return self.__decision

    def menu_inicial(self):
        """Exibe o menu inicial e retorna a decisão do usuário."""
        self.clear_screen()
        label = tk.Label(self.root, text="===> SELECIONE A OPÇÃO DESEJADA <===")
        label.pack(pady=10)

        def set_decision(decision):
            self.__decision = decision
            self.root.quit()  # Fecha o loop de eventos do Tkinter

        btn_signup = tk.Button(self.root, text="1 - Tornar-se Cliente", command=lambda: set_decision(1))
        btn_signup.pack(pady=5)

        btn_login = tk.Button(self.root, text="2 - Acessar Conta", command=lambda: set_decision(2))
        btn_login.pack(pady=5)

        btn_exit = tk.Button(self.root, text="0 - Sair", command=lambda: set_decision(0))
        btn_exit.pack(pady=5)

        self.root.mainloop()
        return self.__decision
    
    def menu_selecao_conta(self, contas):
        """Exibe as contas como botões para o usuário selecionar uma."""
        self.clear_screen() 

        # Variável local para armazenar a seleção do usuário
        selected_account = tk.StringVar()

        def selecionar_conta(conta_numero):
            """Define a conta selecionada e retorna o número da conta."""
            selected_account.set(conta_numero)
            self.root.quit()  # Fecha o loop principal para continuar a execução

        label = tk.Label(self.root, text="Selecione a conta que deseja acessar:")
        label.pack(pady=10)

        for conta in contas:
            btn_conta = tk.Button(self.root, text=f"Conta {conta.numeroConta}", command=lambda c=conta.numeroConta: selecionar_conta(c))
            btn_conta.pack(pady=5)

        self.root.mainloop()  # Inicia o loop de eventos do Tkinter para capturar a interação do usuário
        number_account = selected_account.get()
        messagebox.showinfo("Conta selecionada",f"Acessando a conta:{number_account}")

        return number_account  # Retorna o número da conta selecionada


    def menu_signup(self):
        """Formulário de cadastro de cliente."""
        user = {}
        user['cpf'] = simpledialog.askstring("Cadastro", "Digite seu CPF")
        user['email'] = simpledialog.askstring("Cadastro", "Digite seu email")
        password_correct = False
        while not password_correct:
            password1 = simpledialog.askstring("Cadastro", "Digite sua senha", show='*')
            password2 = simpledialog.askstring("Cadastro", "Confirme sua senha", show='*')
            if password1 == password2:
                password_correct = True
            else:
                messagebox.showerror("Erro", "As senhas não coincidem")
        user['password'] = password1
        user['name'] = simpledialog.askstring("Cadastro", "Digite seu nome")
        user['born'] = simpledialog.askstring("Cadastro", "Data de nascimento (DD/MM/AAAA)")
        user['address'] = simpledialog.askstring("Cadastro", "Digite seu endereço")
        return user
    
    def menu_usuario(self):
        """Menu para o usuário logado."""
        self.clear_screen()  # Limpa a tela antes de mostrar o menu do usuário
        
        label = tk.Label(self.root, text="===> ESCOLHA A OPÇÃO DESEJADA <===")
        label.pack()

        def set_decision(decision_value):
            self.__decision = decision_value
            self.root.quit()  # Fecha o loop de eventos do Tkinter

        btn_deposito = tk.Button(self.root, text="1 - Realizar depósito", command=lambda: set_decision(1))
        btn_deposito.pack(pady=5)

        btn_saque = tk.Button(self.root, text="2 - Realizar saque", command=lambda: set_decision(2))
        btn_saque.pack(pady=5)

        btn_extrato = tk.Button(self.root, text="3 - Verificar extrato", command=lambda: set_decision(3))
        btn_extrato.pack(pady=5)
        btn_create_account = tk.Button(self.root, text="4 - Create new account", command=lambda: set_decision(4))
        btn_create_account.pack(pady=5)
        btn_create_account = tk.Button(self.root, text="5 - Mudar de conta", command=lambda: set_decision(5))
        btn_create_account.pack(pady=5)


        btn_exit = tk.Button(self.root, text="0 - Sair", command=lambda: set_decision(0))  # Botão de logout
        btn_exit.pack(pady=3)

        self.root.mainloop()  # Aguarda decisão do usuário
        return self.__decision

    def menu_deposito(self):
        """Coleta número da conta e valor para depósito."""
        numero_conta = simpledialog.askstring("Depósito", "Digite o número da conta")
        valor = simpledialog.askfloat("Depósito", "Digite o valor do depósito")
        return (numero_conta, valor)

    def menu_saque(self):
        """Coleta o valor para saque."""
        valor = simpledialog.askfloat("Saque", "Digite o valor que deseja sacar")
        return valor

    def menu_extrato(self, transactions, saldo_atual:float):
        """Exibe o extrato da conta."""
        extrato = "\n".join([f"{transacao}" for transacao in transactions])
        messagebox.showinfo("Extrato", f"===> EXTRATO DA CONTA <===\n{extrato} \n Saldo atual: {saldo_atual}")

    def menu_login(self):
        """Solicita CPF e senha para login."""
        cpf = simpledialog.askstring("Login", "Digite seu CPF")
        senha = simpledialog.askstring("Login", "Digite sua senha", show='*')
        return (cpf, senha)

    def clear_screen(self):
        """Limpa os widgets da tela atual."""
        for widget in self.root.winfo_children():
            widget.destroy()
