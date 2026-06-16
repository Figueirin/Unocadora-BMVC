import os
import json
from models.cliente import Cliente
from models.usuario import Usuario
from models.veiculo import Carro, Moto, Caminhonete
from models.Locacao import Locacao

class GravaDados:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "data")

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)


