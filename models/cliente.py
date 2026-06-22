from models.usuario import Usuario

class Cliente(Usuario):

    def __init__(self, nome: str, cpf: str, telefone: str, username: str, password: str):
        super().__init__(username, password)

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
        import re
        if not valor:
            raise ValueError("O CPF não pode ser vazio")
            
        # Limpa todos os caracteres não numéricos
        valor_limpo = re.sub(r'\D', '', valor)
        
        if len(valor_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos")
            
        # CPFs com todos os dígitos repetidos são inválidos
        if valor_limpo in [str(i)*11 for i in range(10)]:
            raise ValueError("CPF inválido (todos os dígitos são iguais)")
            
        # Validação do primeiro dígito verificador
        soma = sum(int(valor_limpo[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        if resto in (10, 11):
            resto = 0
        if resto != int(valor_limpo[9]):
            raise ValueError("CPF inválido")
            
        # Validação do segundo dígito verificador
        soma = sum(int(valor_limpo[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        if resto in (10, 11):
            resto = 0
        if resto != int(valor_limpo[10]):
            raise ValueError("CPF inválido")
        
        self.__cpf = valor_limpo

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
            "telefone": self.telefone,
            "username": self.username,
            "password": self.password
        }

