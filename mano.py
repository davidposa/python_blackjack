""" Codigo para la clase Mano
"""
from typing import List, Dict
from functools import reduce
from carta import Carta
from otros import unir_str_por_linea


class Mano(object):
    """ Clase para representar manos
    """
    def __init__(self, nombre: str, apuesta: int, cartas: List[Carta]) -> None:
        """ Crea e inicializa la mano
        :param nombre: Nombre de la mano, usado para la representacion en la terminal
        :param apuesta: Apuesta asociada a la mano (es importante que sea en euros o el codigo no funciona)
        :param cartas: Cartas que añadir a la mano al crearla
        """
        self.nombre = nombre
        self.apuesta = apuesta
        self.estado = "Abierta"
        self.cartas = []
        for carta in cartas:
            self.añadir_carta(carta)

    def __str__(self) -> str:
        """ Metodo para representar una mano en la terminal de forma lujosa.
        :return: String con la representacion de la mano
        """
        lin_nom = f"{self.nombre}:"
        lin_val = f"({self.valor})"
        lin_apu = f"{self.apuesta}€"
        lin_estado = f"{self.estado}"
        lineas = [lin_nom, lin_val, lin_apu, lin_estado]
        max_len = max(map(len, lineas))
        info_mano = "\n".join([l.rjust(max_len) for l in lineas])
        return reduce(unir_str_por_linea, [info_mano] + [str(c) for c in self.cartas])
        
    @property
    def valor(self) -> int:
        """ Calcula el valor total de la mano sumando los valores de las 
            cartas que contiene. Intenta contar los ases como 11 puntos
            si puede no cerrar la mano.
        :return: Valor de la mano
        """
        v = sum(c.valor for c in self.cartas)
        # contar ases como 11 puntos si no cierra la mano
        for _ in range(len([c for c in self.cartas if c.numero == " A"])):
            v += 10 if v <= 11 else 0
        return v
    
    def añadir_carta(self, carta: Carta):
        """ Metodo para añadir cartas a la mano. Se encarga de actualizar 
            el estado de la mano despues de añadir la carta.
        """
        self.cartas += [carta]
        if self.valor > 21:
            self.estado = "PASADA"

    def cerrar(self):
        """ Metodo para cerrar la mano.
        """
        self.estado = "Cerrada"

    def doblar(self, carta: Carta):
        """ Metodo para doblar la mano. Dobla la apuesta, cierra la mano 
            y añade una carta.
        """
        self.apuesta = self.apuesta * 2
        self.cerrar()
        self.añadir_carta(carta)

    def separar(self):
        """ Metodo para separar la mano. Solo puede ser llamado si la mano tiene 
            exactamente dos cartas con el mismo valor numerico. Separa la mano
            en dos, con una carta cada una.
        :return: Lista con las dos manos separadas
        """
        return [Mano(self.nombre + l, apuesta=self.apuesta, cartas=[c]) for c, l in zip(self.cartas, ["A", "B"])]
    
    def opciones(self) -> Dict[str, str]:
        """ Metodo para calcular las opciones disponibles para la mano. Las posibles
            opciones son: pedir otra carta (P), cerrar la mano (C), doblar la apuesta (D),
            o separar la mano en dos. Esta ultima solo esta disponible si la mano tiene 
            unicamente dos cartas con el mismo valor numerico.
        :return: Diccionario con las posibles opciones
        """
        if self.estado in ["PASADA", "Cerrada"]:
            return {}
        opcs = {"p": "[P]edir", "c": "[C]errar", "d": "[D]oblar"}
        if len(self.cartas) == 2 and self.cartas[0].valor == self.cartas[1].valor:
            opcs["s"] = "[S]eparar"
        return opcs
    
    def evaluar (self, mano: Self):
        """Metodo para calcular si la mano gana o pierde contra otra mano.
        return: 1 si la mano gana, -1 si pierde, y 0 si nadie gana
        """
        if ((self.estado  == "PASADA"and mano.estado == "PASADA") or self.valor == mano.valor):
            return 0
        elif ((mano.estado == "PASADA" or self.valor > mano.valor)) and (self.estado != "PASADA"):
            return self.apuesta
        elif self.estado == "PASADA" or mano.valor > self.valor:
            return self.apuesta * -1
