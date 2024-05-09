import textwrap
# from abc import ABC, abstractclassmethod, abstractproperty
from abc import ABC
import abc
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:

    def __init__(self, saldo, numero, agencia, cliente, historico):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('\n@@@ Operação falhou! Saldo insuficiente para sacar. @@@')        

        elif valor > 0:
            self._saldo -= valor
            print('\n === Saque realizado com sucesso! ===')
            return True

        else:
            print('\n @@@ Operação falhou! O valor informado é invalido. @@@')
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n === Deposito realizado com sucesso! ===')

        else:
            print('\n @@@ Operação falhou! O valor informado é invalido. @@@')
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacao if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('\n@@@ Operação falhou! O valor do saque excedeu o limite. @@@')        

        elif excedeu_saques:
            print('\n@@@ Operação falhou! Número máximo de saques excedeu o limite. @@@')  

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agêcia:\t {self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )

class Transacao(ABC):
    @property
    @abc.abstractproperty
    def valor(self):
        pass

    @abc.abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
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
