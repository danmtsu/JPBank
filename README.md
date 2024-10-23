# JPBank System - Sistema Bancário

Este projeto implementa um sistema bancário simples com interface gráfica usando a biblioteca `Tkinter` e gerenciamento de operações financeiras com `Python`. Ele simula funcionalidades básicas de um banco, como criação de contas, depósitos, saques, visualização de extratos e controle de múltiplas contas para um usuário.

## Funcionalidades

- **Criação de Usuário**: Permite o cadastro de novos usuários com nome, CPF, data de nascimento e email.
- **Login de Usuário**: Autenticação de usuário com CPF e senha.
- **Seleção de Contas**: Usuários podem gerenciar múltiplas contas associadas ao seu CPF.
- **Depósito**: Os usuários podem realizar depósitos em suas contas.
- **Saque**: Permite realizar saques, com controle de limites diários.
- **Extrato**: Exibição das transações realizadas em uma conta.
- **Logout**: Possibilidade de deslogar e voltar à tela inicial.

## Arquitetura do Sistema

### ControlBox (Controlador Principal)

A classe `ControlBox` gerencia a lógica do sistema bancário, conectando a interface gráfica com o banco de dados (`Bank`). Ela é responsável por:
- Controlar a navegação entre as diferentes telas da interface.
- Gerenciar as operações bancárias de maneira segura com uso de **threads** e mecanismos de sincronização como **mutex** (Lock).
- Interagir com o banco de dados para operações de login, criação de conta, saques, depósitos, etc.

### Interface (View)

A interface gráfica é construída usando a biblioteca `Tkinter`, fornecendo uma interface intuitiva para interação do usuário. As principais telas incluem:
- Tela de Login
- Tela de Cadastro de Usuário
- Menu Principal do Usuário
- Seleção de Contas
- Depósitos e Saques
- Visualização de Extrato

### Bank (Modelo de Dados)

A classe `Bank` é responsável por armazenar e gerenciar os dados de usuários, contas e transações. As operações financeiras são realizadas por meio de métodos que interagem com a estrutura de dados.

## Bibliotecas Utilizadas

### Tkinter
Utilizada para criar a interface gráfica do usuário (GUI). Ela oferece os componentes visuais, como botões, labels, caixas de texto, etc.

- [Documentação oficial do Tkinter](https://docs.python.org/3/library/tkinter.html)

### Threading
A biblioteca `threading` é utilizada para garantir que as operações bancárias como depósitos, saques e criação de contas aconteçam de forma assíncrona, sem travar a interface do usuário. Com o uso de **ThreadPoolExecutor**, criamos threads para operações específicas que podem ocorrer simultaneamente, sem bloquear a interface.

- [Documentação oficial de threading](https://docs.python.org/3/library/threading.html)
  
### Lock (Mutex)
Um **Mutex** é utilizado para garantir que dados críticos, como o saldo da conta, sejam protegidos durante modificações concorrentes. Isso evita que duas ou mais threads alterem o saldo simultaneamente, causando inconsistências.

- [Documentação de Lock](https://docs.python.org/3/library/threading.html#lock-objects)

## Gerenciamento de Threads

### Threads de Operações Bancárias

Cada operação sensível, como depósitos, saques e criação de contas, é realizada em uma thread separada para evitar que a interface fique bloqueada enquanto a operação é processada. Para garantir a segurança de dados críticos (como saldo de contas), o **Lock (Mutex)** é utilizado. Exemplos de funções gerenciadas por threads incluem:

- `__thread_deposito`: Realiza depósitos de forma assíncrona, protegendo o saldo da conta com `Lock`.
- `__thread_saque`: Faz saques, verificando o saldo e o número de saques permitidos no dia.
- `__thread_create_user`: Responsável por criar um novo usuário no banco de dados de forma concorrente.

### Exemplo de Uso de Thread:
```python
def __thread_deposito(self, numero_conta, valor: float):
    with self.lock:  # Protege a operação de depósito com um Mutex
        if str(numero_conta).strip() in self.__bank.contas:
            if valor > 0:
                self.__bank.realiza_deposito(numero_conta, valor)
                # Atualiza a interface com a mensagem de sucesso
                self.__menu.root.after(270, self.__menu.alerts, "Depósito", "Depósito realizado com sucesso!")
            else:
                self.__menu.root.after(270, self.__menu.errors, "Depósito", "Valor do depósito inválido")
        else:
            self.__menu.root.after(270, self.__menu.errors, "Depósito", "Conta de destino inexistente")
