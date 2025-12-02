import unittest

from calculadora import Calculadora

class TestCalculadora(unittest.TestCase):

    def setUp(self):
        print("Realizamos prueba")
        self.calculadora = Calculadora(8, 2)

    def test_suma(self):
        print("prueba de suma correcta:")
        self.assertEqual(self.calculadora.get_suma(), 9, 'La suma no es correcta')
        self.assertNotEqual(self.calculadora.get_suma(), 10, 'La suma no es correcta')
    
    def test_suma_erronea(self):
        print("prueba de suma erronea:")
        self.assertNotEqual(self.calculadora.get_suma(), 11, 'La suma es correcta')

    #def test_divison_erronea(self):
        #print("prueba division:")
        #calculadora = Calculadora(8, 0)
        #self.assertNotEqual(calculadora.get_division(), 10, 'La suma es correcta')
                

    def tearDown(self):
        print("Terminamos prueba")

if __name__ == '__main__':
    unittest.main()
