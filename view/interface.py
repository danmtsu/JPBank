import tkinter as tk
from tkinter import messagebox
from bank import Bank

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("JPBank - Sistema Bancário")
        self.root.geometry("400x300")  # Define o tamanho da janela

        self.bank = Bank()  # Instância do banco
        self.create_initial_screen()
    
    def add_placeholder(self, entry, placeholder):
        """Adiciona um placeholder em um campo Entry."""
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.restore_placeholder(entry, placeholder))

    def clear_placeholder(self, entry, placeholder):
        """Remove o placeholder ao focar no campo, se o texto for igual ao placeholder."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def restore_placeholder(self, entry, placeholder):
        """Restaura o placeholder se o campo estiver vazio."""
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    def create_initial_screen(self):
        # Limpa a tela atual (se houver widgets anteriores)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cria o menu inicial
        tk.Label(self.root, text="===> SELECIONE A OPÇÃO DESEJADA <===", font=("Arial", 12)).pack(pady=20)
        tk.Button(self.root, text="1 - Tornar-se Cliente", command=self.menu_signup).pack(pady=5)
        tk.Button(self.root, text="2 - Acessar Conta", command=self.menu_login).pack(pady=5)
        tk.Button(self.root, text="0 - Sair", command=self.root.quit).pack(pady=5)

    def menu_signup(self):
        # Limpar tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Formulário de inscrição
        label = tk.Label(self.root, text="Cadastro de Cliente")
        label.pack(pady=10)

        self.cpf = tk.Entry(self.root, fg='grey')
        self.add_placeholder(self.cpf, "Digite seu CPF")
        self.cpf.pack(pady=5)

        self.email = tk.Entry(self.root, fg='grey')
        self.add_placeholder(self.email, "Digite seu email")
        self.email.pack(pady=5)

        self.password = tk.Entry(self.root, show="*", fg='grey')
        self.add_placeholder(self.password, "Digite sua senha")
        self.password.pack(pady=5)

        self.password_confirm = tk.Entry(self.root, show="*", fg='grey')
        self.add_placeholder(self.password_confirm, "Confirme sua senha")
        self.password_confirm.pack(pady=5)

        btn_submit = tk.Button(self.root, text="Cadastrar", command=self.submit_signup)
        btn_submit.pack(pady=5)

        btn_back = tk.Button(self.root, text="Voltar", command=self.create_initial_screen)
        btn_back.pack(pady=5)

    def submit_signup(self):
        # Obtenção dos dados de entrada
        cpf = self.cpf.get()
        email = self.email.get()
        password = self.password.get()
        password_confirm = self.password_confirm.get()

        # Remove placeholders antes da validação
        if cpf == "Digite seu CPF":
            cpf = ""
        if email == "Digite seu email":
            email = ""
        if password == "Digite sua senha":
            password = ""
        if password_confirm == "Confirme sua senha":
            password_confirm = ""

        # Verifica se as senhas coincidem
        if password != password_confirm:
            tk.messagebox.showerror("Erro", "As senhas não coincidem")
            return

        # Valida se os campos estão preenchidos
        if not cpf or not email or not password:
            tk.messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        # Aqui você pode integrar com a lógica de cadastro de usuários
        tk.messagebox.showinfo("Sucesso", f"Usuário {email} cadastrado com sucesso!")

        # Volta para a tela inicial após o cadastro
        self.create_initial_screen()


    def menu_login(self):
        # Limpar tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tela de login
        label = tk.Label(self.root, text="Login do Cliente")
        label.pack(pady=10)

        self.cpf_login = tk.Entry(self.root)
        self.cpf_login.insert(0, "Digite seu CPF")
        self.cpf_login.pack(pady=5)

        self.senha_login = tk.Entry(self.root, show="*")
        self.senha_login.insert(0, "Digite sua senha")
        self.senha_login.pack(pady=5)

        btn_login = tk.Button(self.root, text="Login", command=self.submit_login)
        btn_login.pack(pady=5)

        btn_back = tk.Button(self.root, text="Voltar", command=self.create_initial_screen)
        btn_back.pack(pady=5)

    def submit_login(self):
        cpf = self.cpf_login.get()
        password = self.senha_login.get()

        try:
            if self.bank.verify_user(cpf, password):  # Método a ser implementado na classe Bank
                messagebox.showinfo("Login", "Login bem-sucedido!")
                self.menu_usuario()  # Chama a função que exibe o menu do usuário
            else:
                messagebox.showerror("Erro", "CPF ou senha incorretos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def menu_usuario(self):
        # Limpa a tela anterior
        for widget in self.root.winfo_children():
            widget.destroy()

        # Adiciona opções para depósito, saque, extrato, etc.
        tk.Button(self.root, text="Realizar Depósito", command=self.menu_deposito).pack(pady=5)
        tk.Button(self.root, text="Realizar Saque", command=self.menu_saque).pack(pady=5)
        tk.Button(self.root, text="Ver Extrato", command=self.menu_extrato).pack(pady=5)

    def menu_deposito(self):
        messagebox.showinfo("Depósito", "Depósito realizado com sucesso!")

    def menu_saque(self):
        messagebox.showinfo("Saque", "Saque realizado com sucesso!")

    def menu_extrato(self):
        messagebox.showinfo("Extrato", "Aqui está seu extrato!")
