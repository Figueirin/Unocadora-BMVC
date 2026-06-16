import os
import json
from models.cliente import Cliente
from models.usuario import Usuario
from models.veiculo import Carro, Moto, Caminhonete
from models.locacao import Locacao

class GravaDados:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "data")

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)


    def _obter_caminho(self, arquivo: str) -> str:
        return os.path.join(self.data_dir, arquivo)

    def ler_json(self, arquivo: str) -> list:
        caminho = self._obter_caminho(arquivo)

        if not os.path.exists(caminho):
            return []

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        
        except(json.JSONDecodeError, IOError):
            return []

    
    def _salvar_json(self, arquivo: str, dados: list):
        caminho = self._obter_caminho(arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def salvar_clientes(self, clientes:list[Cliente]):
        dados = [c.to_dict() for c in clientes]
        self._salvar_json("clientes.json", dados)

    def carregar_clientes(self) -> list[Cliente]:

        dados = self._salvar_json("clientes.json")
        clientes = []
        for item in dados:
            try:
                c = Cliente(item["nome"], item["cpf"], item["telefone"])
                clientes.append(c)
            except ValueError:

                continue

        return clientes

    def salvar_usuarios(self, usuario:list[Usuario]):
        dados = [c.to_dict() for c in usuario]
        self._salvar_json("usuarios.json", dados)

    def carregar_usuario(self) -> list[Usuario]:

        dados = self._salvar_json("usuarios.json", dados)
        usuarios = []
        for item in dados:
            try:
                c = Cliente(item["username"], item["password"])
                usuarios.append(c)
            except ValueError:
                continue

        return usuarios

    def salvar_veiculos(self, veiculos: list):
        dados = [v.to_dict() for v in veiculos]
        self._salvar_json("veiculos.json", dados)

    def carregar_veiculos(self) -> list:
        dados = self.ler_json("veiculos.json")
        veiculos = []

        for item in dados:
            tipo = item.get("tipo")
            placa = item.get("placa")
            marca = item.get("marca")
            modelo = item.get("modelo")
            ano = item.get("ano")

            try:
                if tipo == "carro":
                    v = Carro(placa, modelo, marca, ano)
                elif tipo == "moto":
                    v = Moto(placa, modelo, marca, ano)
                elif tipo == "caminhonete":
                    v = Caminhonete(placa, modelo, marca, ano)
                else:
                    continue
                
                veiculos.append(v)

            except ValueError:
                continue
        return  veiculos


