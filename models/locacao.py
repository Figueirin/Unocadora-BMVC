from datetime import datetime
from models.cliente import Cliente
from models.veiculo import Veiculo

class Locacao:
    def __init__(self, cliente: Cliente, veiculo: Veiculo, data_inicio: str, data_final: str):
        self.cliente = cliente
        self.veiculo = veiculo
        self.data_inicio = data_inicio
        self.data_final = data_final

    def calcular_total(self) -> float:

        d_inicio = datetime.strptime(self.data_inicio, "%Y-%m-%d")
        d_fim = datetime.strptime(self.data_fim, "%Y-%m-%d")
        qtd_dias = (d_fim - d_inicio).days
        qtd_dias = max(1, qtd_dias)

        return qtd_dias * self.veiculo.calcular_diaria()

    def to_dict(self) -> dict:
        return {
            "cliente_cpf": self.cliente.cpf,
            "veiculo_placa": self.veiculo.placa,
            "data_inicio": self.data_inicio,
            "data_final": self.data_final
        }