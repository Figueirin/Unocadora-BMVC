from abc import ABC, abstractmethod

class Veiculo(ABC):
    def __init__(self, placa: str, modelo: str, marca: str, ano: int):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.ano = ano

    @property
    def placa(self) -> str:
        return self.__placa

    @placa.setter
    def placa(self, valor: str):
        if not valor or len(valor.strip()) < 5:
            raise ValueError("Placa Invalida")
        self.__placa = valor.strip().upper()

    @property
    def modelo(self) -> str:
        return self.__modelo
    
    @modelo.setter
    def modelo(self, valor: str):
        if not valor or len(valor.strip()) == 0:
            raise ValueError("Modelo não poder ser vazio")
        self.__modelo = valor

    @property
    def marca(self) -> str:
        return self.__marca

    @marca.setter
    def marca(self, valor: str):
        if not valor or len(valor.strip()) == 0:
            raise ValueError("Marca não pode ser vazia")
        self.__marca = valor
    
    @property
    def ano(self) -> int:
        return self.__ano

    @ano.setter
    def ano(self, valor: int):
        if valor <= 0:
            raise ValueError("Insira um ano valido")
        self.__ano = valor

    @abstractmethod
    def calcular_diaria(self) -> float:
        pass

    def to_dict(self) -> dict:
        return{
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "tipo": self.__class__.__name__.lower()
        }
        
class Carro(Veiculo):
    def calcular_diaria(self) -> float:
        return 120.0

class Moto(Veiculo):
    def calcular_diaria(self) -> float:
        return 80.0

class Caminhonete(Veiculo):
    def calcular_diaria(self) -> float:
        return 180.0

