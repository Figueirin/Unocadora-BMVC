from models.grava_dados import GravaDados
from models.cliente import Cliente
from models.locacao import Locacao
from models.veiculo import Carro, Moto, Caminhonete
from models.usuario import Usuario

class Aplicacao:
    def __init__(self):
        self.db = GravaDados()
        self.clientes = self.db.carregar_clientes()
        self.veiculos = self.db.carregar_veiculos()
        self.usuarios = self.db.carregar_usuarios()
        self.locacoes = self.db.carregar_locacoes(self.clientes, self.veiculos)

    def login(self, username, password) -> bool:
        for u in self.usuarios:
            if u.username == username.strip().lower() and u.verificar_senha(password):
                return True
        
        for c in self.clientes:
            if c.username == username.strip().lower() and c.verificar_senha(password):
                return True

        return False

    def cadastrar_cliente(self, nome: str, cpf: str, telefone: str, username: str, password: str):

        username_limpo = username.strip().lower()

        for u in self.usuarios:
            if u.username == username_limpo:
                raise ValueError("Nome de usuario já cadastrado")

        for c in self.clientes:
            if c.username == username_limpo:
                raise ValueError("Nome de usuario já cadastrado")
            if c.cpf == cpf:
                raise ValueError("CPF ja cadastrado")

        novo_cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone, username=username_limpo, password=password)
        self.clientes.append(novo_cliente)
        self.db.salvar_clientes(self.clientes)

    def obter_cliente_por_user(self, username: str) -> Cliente:
        username_limpo = username.strip().lower()
        for c in self.clientes:
            if c.username == username_limpo:
                return c
        return None

    def cadastrar_veiculo(self, placa: str, modelo: str, marca: str, ano: int, tipo: str):
        for v in self.veiculos:
            if v.placa == placa.upper():
                raise ValueError("Placa de veiculo ja cadastrada")

        t = tipo.lower()
        if t == "carro":
            novo_veiculo = Carro(placa, modelo, marca, ano)
        elif t == "moto":
            novo_veiculo = Moto(placa, modelo, marca, ano)
        elif t == "caminhonete":
            novo_veiculo = Caminhonete(placa, modelo, marca, ano)
        else:
            raise ValueError("Tipo de Veiculo Invalido")

        self.veiculos.append(novo_veiculo)
        self.db.salvar_veiculos(self.veiculos)

    def cadastrar_locacao(self, cliente_cpf: str, veiculo_placa: str, data_inicio: str, data_final: str):
        cliente = None
        for c in self.clientes:
            if c.cpf == cliente_cpf:
                cliente = c
                break
        
        veiculo = None
        for v in self.veiculos:
            if v.placa == veiculo_placa.upper():
                veiculo = v
                break

        if not cliente:
            raise ValueError("Cliente nao encontrado")
        
        if not veiculo:
            raise ValueError("Veiculo nao encontrado")

        nova_locacao = Locacao(cliente, veiculo, data_inicio, data_final)
        self.locacoes.append(nova_locacao)
        self.db.salvar_locacoes(self.locacoes)

        
