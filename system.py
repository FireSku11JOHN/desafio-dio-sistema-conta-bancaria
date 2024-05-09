import textwrap

def menu ():
    menu = '''\n
    ========= Opções =========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [nu]\tNovo usuário
    [q]\tSair
        
        => '''
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito:\tR${valor:.2f}\n'
        print('\n Depósito realizado com sucesso!')

    else:
        print('\n Operação falhou! O valor informado é inválido')

    return saldo, extrato

def sacar(*,saldo,valor,extrato,limite,numero_saques,
limite_saque,):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_saques >= limite_saque

    if excedeu_saldo:
            print('\nOperação falhou! Saldo insuficiente para sacar!')

    elif excedeu_limite:
        print('\nOperação falhou! O valor do saque exede o limite!')

    elif excedeu_saque:
        print('\nOperação falhou! Número limite de saques diários atingidos!')

    elif valor >0:   
        saldo -= valor
        extrato += f'\tSaque: R${valor:.2f}\n'
        numero_saques += 1
        print(f'\nVoçê sacou R${valor:.2f}. Seu saldo atual é de R${saldo:.2}.\n')

    else:
        print('\nOperação falhou! O valor informado é inválido.')

    return saldo, extrato

def exibir_extrato(saldo,/, *, extrato):
    print('\n========== EXTRATO ==========')
    print('Não foram realizadas movimetações.' if not extrato else extrato)
    print(f'\nSaldo \t\t {saldo:.2f}')
    print('===============================')

def criar_usuario(usuarios):
    cpf = input('Informe seu CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\nJá existe um usuario com esse CPF!')
        return
    
    nome = input('Nome completo: ')
    data_nascimento = input('Data de nascimento (dd-mm-aaaa): ')
    endereco = input('Endereço: ')

    usuarios.append({'nome': nome,'data_nascimento': data_nascimento,'cpf': cpf ,'endereco': endereco})

    print ('Usuario criado!')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe seu CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\nConta criada!')
        return {'agencia': agencia, 'usuario': usuario, 'numero_conta': numero_conta}
    
    print('\nUsuário não encontrado!')

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    usuarios =[]
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input('Informe o valor do deposito: R$ '))
            saldo, extrato = depositar(saldo, valor , extrato)

        elif opcao == 's':
            valor = float(input('Informe o valor do saque: R$ '))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saque=LIMITE_SAQUES,
            )

        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 'nu':
            criar_usuario(usuarios)

        elif opcao == 'nc':
            numero_conta = len(contas) +1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                conta.append(contas)

        elif opcao == 'q':
            break

        else:
            print('Opção iválida! Tente novamente')

main()
