class Boleto:

    def  __init__ (self, titular, valor, nome, vencimento):
        self.titular = titular
        self.valor = valor
        self.nome = nome
        self.vencimento = vencimento

    def pagar(self, conta_logada, lista_boletos):
        if self.valor <= conta_logada.saldo:
            conta_logada.sacar(self.valor)
            conta_logada.historico.append(f"Pagamento de boleto: -{self.valor:.2f} ({self.nome})")
            print(f"Boleto de {self.nome} no valor de R$ {self.valor:.2f} vencido em {self.vencimento} pago com sucesso!")
            lista_boletos.remove(self)
        else:
            print(f"Saldo insuficiente para pagar o boleto de {self.nome}.")
                
