class Cliente:
    def __init__(self, nome: str, cpf: str, telefone: str):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str):
        if not valor or len(valor.strip()) == 0:
            raise ValueError("O nome nao pode ser vazio")

        self.__nome = valor

    @property
    def cpf(self) -> str:
        return self.__cpf
    
    @cpf.setter
    def cpf(self, valor: str):
        if not valor or len(valor.strip()) < 11:
            raise ValueError("O CPF deve conter 11 numeros")
        
        self.__cpf = valor

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, valor: str):
        if not valor or len(valor.strip()) < 9:
            raise ValueError("Digite um numero valido")
        self.__telefone = valor

    def to_dict(self):
        return{
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone
        }