def validar_escolha(valor_minimo, valor_maximo):
    while True:
        try: 
            escolha_usuario = int(input("Escolha uma opção: "))
            if valor_minimo <= escolha_usuario <= valor_maximo:
                return escolha_usuario
            else:
                print("\nOpção inválida, por favor verifique as informações e tente novamente.\n")
        except ValueError:
            print("Entrada inválida, por favor digite um número inteiro.")

def validar_entrada_cpf(valor_maximo):
    while True:
        try: 
            cpf = str(input("Insira seu CPF com apenas números: "))
            if len(cpf) == valor_maximo:
                return cpf
            else:
                print("\nO CPF deve conter 11 números, tente novamente\n")
        except ValueError:
            print("Entrada inválida, por favor digite apenas números.")

def validar_entrada_nome():
    while True:
        try: 
            nome = input("Insira seu nome completo: ")
            if nome.replace(" ", "").isalpha():
                return nome
            else:
                print("\nApenas letras são válidas, tente novamente.\n")
        except ValueError:
            print("Entrada inválida, por favor digite apenas letras.")

def validar_entrada_data_nascimento(valor_maximo):
    while True:
        try: 
            data_de_nascimento = input("Inisira da data como o exemplo (DD/MM/AAAA): ")
            if len(data_de_nascimento) == valor_maximo:
                return data_de_nascimento
            else:
                print("\nO data deve conter 10 caracteres, EX: 20/20/2024\n")
        except ValueError:
            print("Entrada inválida, por favor verifique e tente novamente.")

def menu_pagina_inicial():
    print('''==============Seja bem-vindo ao banco DIO!==============\n')
    Menu:
        1 - Cadastrar
        2 - Solicitar Nova Conta
        3 - Exibir Contas Cadastradas
        4 - Depositar
        5 - Sacar
        6 - Exibir Extrato
        7 - Sair
    ''')

def criar_usuario(usuarios_cadastrados):
    print("\n===========Cadastro de Usuário===========\n")
    cpf = validar_entrada_cpf(11)
    usuario_existente = buscar_usuario(cpf, usuarios_cadastrados)

    if usuario_existente:
        print(f"Informe outro CPF, já existe uma conta com esse mesmo CPF!")
        return

    nome = validar_entrada_nome()
    data_nascimento = validar_entrada_data_nascimento(10)
    endereco_usuario = input("Por favor informe seu endereco como o exemplo => (Rua, Cidade - Estado): ")

    novo_usuario = {
        "nome" : nome,
        "data_nascimento" : data_nascimento,
        "cpf" : cpf,
        "endereco" : endereco_usuario
    }

    usuarios_cadastrados.append(novo_usuario)

    print(f"\nSeja bem-vindo {nome}, sua conta foi criada com sucesso. Você já pode utilizar os benefícios.\n")

def criar_nova_conta(agencia, numero_da_conta, contas_de_usuarios):
    cpf = validar_entrada_cpf(11)
    usuario = buscar_usuario(cpf, contas_de_usuarios)
    if usuario:
        nova_conta =  {
        "agencia": agencia, 
        "numero_da_conta": numero_da_conta,
        "usuario" : usuario
        }
        print(f"\nNova conta adicionada com sucesso, você pode verificar as contas vinculadas ao seu CPF em (Exibir Contas Cadastradas)\n")
        return nova_conta
    else:
        print("\nUsuário não encontrado, verifique as informações ou crie uma conta.\n")
    return None

def buscar_usuario(cpf, usuarios_cadastrados):
    for usuario in usuarios_cadastrados:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def listar_contas(contas_de_usuarios):
    if contas_de_usuarios:
        for conta in contas_de_usuarios:
            print(f"\nContas cadastradas no CPF {conta["usuario"]["cpf"]}: Agência: {conta['agencia']}, Conta: {conta['numero_da_conta']}\n")
    else:
        print("\nNão há contas cadastradas.\n")

def depositar(saldo, valor, extrato, /):
    if saldo >= 0:
        saldo += valor
        extrato += f"\nVocê realizou um depósito no valor de: R${valor:.2f}"
        print(f"\nO depósito de R${valor} foi realizado com sucesso\n")
    else:
        print("n\A operação falhou, por favor tente novamente.\n")
    return saldo, extrato
    
def sacar(*, saldo, valor, extrato, limite, numero_de_saques, limite_de_saques):
    execedeu_limite_de_saldo = valor > saldo
    execedeu_limite_de_saque = valor > limite
    execedeu_limite__diario_de_saque = numero_de_saques >= limite_de_saques

    if execedeu_limite_de_saldo:
        print(f"\nSaldo insuficiente para saque, o valor do seu saldo é: R${saldo}, faça um depósito primeiro!\n")
    elif execedeu_limite_de_saque:
        print(f"Desculpe mas você excedeu o limite de valor para saque, seu limite é: R${limite}.")
    elif execedeu_limite__diario_de_saque:
        print(f"\nDesculpe mas você excedeu o limite diário para saque, você pode sacar apenas 3x por dia.\n")
    elif valor > 0:
        saldo -= valor  
        extrato += f"\nVocê realizou um saque no valor de: R${valor:.2f}"
        numero_de_saques += 1
        print(f"\nO saque de R${valor} foi realizado com sucesso\n")
    else:
        print("Verifique os valores digitados e tente novamente")
    
    return saldo, extrato, numero_de_saques
        
def exibir_extrato(saldo, /, *, extrato):
    print("\n==============Extrato==============\n")
    if not extrato: 
        print("Não foi realizado nenhuma operação de saques ou depósitos\n")
    else:
        print(f"Saldo atual: R${saldo}")
        print(f"{extrato}\n")

def main():
    AGENCIA = '0001'
    LIMITE_DE_SAQUES = 3

    saldo = 0
    limite = 1500.00
    extrato = ''
    numero_de_saques = 0
    contas_de_usuarios = []
    usuarios_cadastrados = []

    while True:
        menu_pagina_inicial()
        numero_da_operacao = validar_escolha(1,7)

        if numero_da_operacao == 1:
            criar_usuario(usuarios_cadastrados)
        elif numero_da_operacao == 2:
            numero_da_conta = len(contas_de_usuarios)+1
            conta_de_usuario = criar_nova_conta(AGENCIA, numero_da_conta, usuarios_cadastrados)
            if conta_de_usuario:
                contas_de_usuarios.append(conta_de_usuario)
        elif numero_da_operacao == 3:
            listar_contas(contas_de_usuarios)
        elif numero_da_operacao == 4:
            valor = float(input("Informe o valor do depósito:R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif numero_da_operacao == 5:
            valor = float(input("Informe o valor do saque:R$ "))
            saldo, extrato, numero_de_saques = sacar(
            saldo = saldo,
            valor = valor,
            extrato = extrato,
            limite = limite,
            limite_de_saques = LIMITE_DE_SAQUES,
            numero_de_saques = numero_de_saques,
            )
        elif numero_da_operacao == 6:
            exibir_extrato(saldo, extrato = extrato)
        else:
            numero_da_operacao == 7
            print("Programa finalizado com sucesso!")
            break

# =========================== Acima as Funções ==================================

main()


