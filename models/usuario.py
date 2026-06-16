class Usuario:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, valor: str):
        if not valor in len(valor.strip()) == 0:
            raise ValueError("O nome de usuario nao pode ser vazio")
        
        self.__username = valor.strip().lower()

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, valor: str):
        if not valor in len(valor.strip()):
            raise ValueError("A senha nao pode ser vazia")

        self.__password = valor
        
    def to_dict(self) -> dict:
        return{
            "username": self.username,
            "password": self.password
        }
