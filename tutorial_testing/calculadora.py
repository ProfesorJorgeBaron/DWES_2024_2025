class Calculadora:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_suma(self):
        return self.a + self.b

    def get_resta(self):
        return self.a - self.b

    def get_multiplica(self):
        return self.a * self.b

    def get_division(self):
        return self.a / self.b