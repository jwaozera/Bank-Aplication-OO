class Conta:
    #toda vez que criar um novo usuário precisa chamar o construtor
    def __init__(self, nome, senha, saldo_inicial, talao_cheque):
        self.nome = nome
        self.senha = senha
        self.saldo = saldo_inicial
        self.saldo_dolar = 0.0
        self.historico = []
        self.talao_cheque = talao_cheque
        self.metas = []

    #não está nos requisitos mas coloquei por uma boa prática
    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
        else:
            raise ValueError("Saldo insuficiente para saque.")

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
        else:
            raise ValueError("Valor de depósito deve ser positivo.")
    
    def consultar_saldo(self):
        return self.saldo
    
    def consultar_saldo_dolar(self):
        return self.saldo_dolar
    
    def verificar_talao_cheque(self):
        if self.talao_cheque == 0:
            print("Você não pediu um talão de cheque esse mês.")
            
            resposta = input("Deseja adquirir um? (s/n): ").strip().lower()
            if resposta == 's':
                self.talao_cheque = 1
                print("Talão de cheque adquirido com sucesso!")
                self.historico.append("Talão de cheque adquirido.")
            else:
                print("Você optou por não adquirir um talão de cheque.")

        else:
            print("Você já pediu um talão de cheque esse mês.")
            resposta = input("Deseja solicitar outro? (s/n): ").strip().lower()
            if resposta == 's':
                self.sacar(10)  #custo de R$10 para solicitar um novo talão
                self.talao_cheque += 1
                print("Novo talão de cheque solicitado com sucesso!")
                self.historico.append("Talão de cheque adquirido.")
            else: 
                print("Você optou por não solicitar outro talão de cheque.")
