""" Codigo para la clase Carta
"""
from externo import CartaBase


class Carta(CartaBase):
    """ Clase para representar una carta. Hereda de la clase CartaBase y 
        la expande con metodos para representarla de forma lujosa.
    """
    def __init__(self, ind: int):
        """ Crea la carta con su indice en el mazo y calcula el indice
            que le corresponde dentro de una baraja individual (0-51).
        :param ind: El indice de la carta dentro del mazo.
        """
        super().__init__(ind)
        self.ind_bar = self.ind % 52 

    def __str__(self):
        """ Metodo para representar la carta de manera lujosa en la terminal.
            Utiliza caracteres Unicode para formar los bordes.
        :return: String con la representacion de la carta
        """
        borde_arriba = "\u256D\u2500\u2500\u2500\u256E\n"
        lin_num = f"\u2502 {self.numero}\u2502\n"
        lin_palo = f"\u2502{self.palo}  \u2502\n"
        borde_abajo = "\u2570\u2500\u2500\u2500\u256F"
        return "".join([borde_arriba, lin_num, lin_palo, borde_abajo])
    
    @property
    def palo(self) -> str:
        """ Este metodo calcula el palo correspondiente a una carta 
            basandose en su indice dentro de la baraja (0-51).
            Definimos de manera arbitraria el orden de la baraja como:
            treboles -> picas -> diamantes -> corazones.
        :return: Caracter Unicode representando el palo de la carta.
        """
        palos = ["\u2663", "\u2660", "\u2666", "\u2665"]
        return palos[self.ind_bar // 13]
    
    @property
    def numero(self) -> str:
        """ Metodo que calcula el numero que corresponde a la carta basandose
            en su indice. El indice 0 corresponde al as ('A') y los indices 
            10, 11 y 12 a las figuras ('J', 'Q' y 'K').
            Asegura que sea un string de 2 caracteres para hacer mas facil la
            representacion de la carta en la consola.
        :return: String correspondiente al numero de la carta.
        """
        nums = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']
        return nums[self.ind // 13]