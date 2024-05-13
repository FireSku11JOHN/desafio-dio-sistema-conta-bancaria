import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
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

def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return

    valor = float(input('Informe o valor do deposito: '))
    transacao = Depositar(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return

    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\n========== EXTRATO ==========')
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = 'Não foram realizadas movimetações.' 

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f'\nSaldo:\n\t R${conta.saldo:.2f}')
    print('===============================')

def criar_usuario(clientes):
    cpf = input('Informe seu CPF (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\nJá existe um usuario com esse CPF!')
        return
    
    nome = input('Nome completo: ')
    data_nascimento = input('Data de nascimento (dd-mm-aaaa): ')
    endereco = input('Endereço: ')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print ('Usuario criado!')

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\n@@@ Cliente não possui conta! @@@')
        return

    return cliente.contas[0]

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)    
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n=== Conta criada com sucesso! ===')

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'nu':
            criar_cliente(clientes)

        elif opcao == 'nc':
            numero_conta = len(contas) +1
            conta = criar_conta(numero_conta, clientes, contas)

        elif opcao == 'q':
            break

        else:
            print('Opção iválida! Tente novamente')

main()
