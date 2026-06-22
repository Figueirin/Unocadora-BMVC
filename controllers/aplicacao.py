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
        # Limpa o CPF de entrada antes da comparação para garantir compatibilidade
        import re
        cpf_limpo = re.sub(r'\D', '', cliente_cpf)
        for c in self.clientes:
            if c.cpf == cpf_limpo:
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

        # Validação do período de datas
        from datetime import datetime
        try:
            d_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            d_fim = datetime.strptime(data_final, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de datas inválido. Use o formato AAAA-MM-DD")

        if d_fim < d_inicio:
            raise ValueError("A data de devolução não pode ser anterior à data de início")

        # Validação de sobreposição de reservas para o mesmo veículo
        for l in self.locacoes:
            if l.veiculo.placa == veiculo.placa:
                l_inicio = datetime.strptime(l.data_inicio, "%Y-%m-%d")
                l_fim = datetime.strptime(l.data_final, "%Y-%m-%d")
                if d_inicio <= l_fim and d_fim >= l_inicio:
                    raise ValueError(f"Este veículo já está alugado no período de {l.data_inicio} a {l.data_final}")

        nova_locacao = Locacao(cliente, veiculo, data_inicio, data_final)
        self.locacoes.append(nova_locacao)
        self.db.salvar_locacoes(self.locacoes)

    def obter_veiculos_disponiveis(self, data_inicio: str, data_final: str) -> list:
        if not data_inicio or not data_final:
            return self.veiculos

        from datetime import datetime
        try:
            d_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            d_fim = datetime.strptime(data_final, "%Y-%m-%d")
        except ValueError:
            return self.veiculos

        if d_fim < d_inicio:
            raise ValueError("A data final deve ser posterior ou igual à data de início")

        disponiveis = []
        for v in self.veiculos:
            overlap = False
            for l in self.locacoes:
                if l.veiculo.placa == v.placa:
                    l_inicio = datetime.strptime(l.data_inicio, "%Y-%m-%d")
                    l_fim = datetime.strptime(l.data_final, "%Y-%m-%d")
                    if d_inicio <= l_fim and d_fim >= l_inicio:
                        overlap = True
                        break
            if not overlap:
                disponiveis.append(v)
        return disponiveis

        
