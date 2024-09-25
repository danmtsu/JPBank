from bank import Bank

def main():
    bank = Bank()
    numeroConta= int(input("digite o numero da conta"))
    
    while numeroConta!= 0:
        bank.criaConta(numeroConta,bank.gerar_numero_agencia())
        numeroConta= int(input("digite o numero da conta: "))
        print(bank.contas, bank.today_formatted)

main()