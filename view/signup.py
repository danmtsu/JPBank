import tkinter as tk
from tkinter import messagebox

class Signup:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Usuário")
        self.root.geometry("400x500")
        
        # Contador de tentativas
        self.tentativas = 0
        self.limite_tentativas = 3

        # Campos do formulário
        self.label_cpf = tk.Label(root, text="CPF:")
        self.label_cpf.pack(pady=5)
        self.entry_cpf = tk.Entry(root)
        self.entry_cpf.pack(pady=5)

        self.label_email = tk.Label(root, text="Email:")
        self.label_email.pack(pady=5)
        self.entry_email = tk.Entry(root)
        self.entry_email.pack(pady=5)

        self.label_senha = tk.Label(root, text="Senha:")
        self.label_senha.pack(pady=5)
        self.entry_senha = tk.Entry(root, show="*")
        self.entry_senha.pack(pady=5)

        self.label_confirm_senha = tk.Label(root, text="Confirme sua senha:")
        self.label_confirm_senha.pack(pady=5)
        self.entry_confirm_senha = tk.Entry(root, show="*")
        self.entry_confirm_senha.pack(pady=5)

        self.label_nome = tk.Label(root, text="Nome:")
        self.label_nome.pack(pady=5)
        self.entry_nome = tk.Entry(root)
        self.entry_nome.pack(pady=5)

        self.label_data_nascimento = tk.Label(root, text="Data de nascimento (DD/MM/AAAA):")
        self.label_data_nascimento.pack(pady=5)
        self.entry_data_nascimento = tk.Entry(root)
        self.entry_data_nascimento.pack(pady=5)

        self.label_endereco = tk.Label(root, text="Endereço:")
        self.label_endereco.pack(pady=5)
        self.entry_endereco = tk.Entry(root)
        self.entry_endereco.pack(pady=5)

        # Botão de submissão
        self.submit_button = tk.Button(root, text="Cadastrar", command=self.submit_form)
        self.submit_button.pack(pady=10)

    def submit_form(self):
        try:
            # Coleta os dados
            cpf = self.entry_cpf.get()
            email = self.entry_email.get()
            senha = self.entry_senha.get()
            confirm_senha = self.entry_confirm_senha.get()
            nome = self.entry_nome.get()
            data_nascimento = self.entry_data_nascimento.get()
            endereco = self.entry_endereco.get()

            # Validações
            if senha != confirm_senha:
                self.tentativas += 1
                raise ValueError("As senhas não coincidem!")
            
            # Se as senhas coincidirem, cria o usuário
            elif cpf is not None and senha is not None:
                user = {
                    'cpf': cpf,
                    'email': email,
                    'password': senha,
                    'name': nome,
                    'born': data_nascimento,
                    'address': endereco
                }
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.clear_screen()  # Fecha o formulário

                return user  # Retorna o usuário criado

        except ValueError as e:
            messagebox.showerror("Erro", f"{str(e)}. Tentativas restantes: {self.limite_tentativas - self.tentativas}")
            
            # Fecha o formulário após o número máximo de tentativas
            if self.tentativas >= self.limite_tentativas:
                messagebox.showwarning("Erro", "Número máximo de tentativas atingido!")
                self.clear_screen()  # Fecha o formulário




    
    def clear_screen(self):
        """Limpa os widgets da tela atual."""
        for widget in self.root.winfo_children():
            widget.destroy()
            
# Criação da janela principal
