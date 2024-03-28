import random
from functools import reduce
from typing import List, Dict

class Estrategia(object):
    # Matrices de estrategia: Filas suma de valores de cartas del jugador (ases = 1), columnas valor carta del croupier
    # Matriz para jugadas con 2 cartas del mismo valor (inicio fila 2)
    MATD = ['S' * 10, *['P' + 'S' * 6 + 'PPP'] * 2, 'P' * 4 + 'SS' + 'P' * 4, 'P' + 'D' * 8 + 'P',
            'P' + 'S' * 6 + 'PPP', 'P' + 'S' * 7 + 'PP', 'S' * 10, 'C' + 'S' * 5 + 'CSSC', 'C' * 10]
    # Matriz para jugadas con algún as (inicio fila 3, suma debe dividirse por 2)
    MATA = [*['P' * 4 + 'DD' + 'P' * 4] * 2, *['PPPDDD' + 'P' * 4] * 2, 'PP' + 'D' * 4 + 'P' * 4,
            'PC' + 'D' * 4 + 'CCPP', *['C' * 10] * 3]
    # Matriz para jugadas sin ases ni duplicados (inicio fila 4)
    MATN = [*['P' * 10] * 5, 'P' + 'D' * 5 + 'P' * 4, 'P' + 'D' * 8 + 'P', 'D' * 10,
            'P' * 3 + 'C' * 3 + 'P' * 4, *['P' + 'C' * 5 + 'P' * 4] * 4, *['C' * 10] * 5]
    # Vector de estrategia de conteo
    CONT = [-2, 2, 2, 2, 3, 2, 1, 0, -1, -2]

    def __init__(self, num_barajas):
        """ Crea e inicializa la estrategia
        :param num_barajas: Número de barajas del mazo utilizado en el juego
        """
        self.num_barajas = num_barajas
        self.num_cartas = 0
        self.cuenta = 0

    def cuenta_carta(self, carta):
        """ Este método se llama automáticamente por el objeto Mazo cada vez
            que se reparte una carta
        :param carta: La carta que se ha repartido
        """
        self.num_cartas += 1
        if self.num_cartas >= 52 * self.num_barajas:
            # Se ha cambiado el mazo
            self.num_cartas = 1
            self.cuenta = 0
        self.cuenta += Estrategia.CONT[carta.valor - 1]

    def apuesta(self, apu_lo, apu_med, apu_hi):
        """ Indica la apuesta que se debe realizar dado el estado del juego.
            Elige entre 3 valores posibles (baja, media y alta)
        :param apu_lo: El valor de la apuesta baja
        :param apu_med: El valor de la apuesta media
        :param apu_hi: El valor de la apuesta alta
        :return: Uno de los 3 valores posibles de apuesta
        """
        barajas_restantes = self.num_barajas - self.num_cartas // 52
        true_count = self.cuenta / barajas_restantes
        if true_count > 1.0:
            return apu_hi
        elif true_count < -1.0:
            return apu_lo
        else:
            return apu_med

    def jugada(self, croupier, jugador):
        """ Indica la mejor opción dada la mano del croupier (que se supone que
            consta de una única carta) y la del jugador
        :param croupier: La carta del croupier
        :param jugador: La lista de cartas de la mano del jugador
        :return: La mejor opción: 'P' (pedir), 'D' (doblar), 'C' (cerrar) o 'S' (separar)
        """
        vc = croupier.valor
        vj = sum(c.valor for c in jugador)
        if len(jugador) == 2 and jugador[0].valor == jugador[1].valor:
            return Estrategia.MATD[vj // 2 - 1][vc - 1]
        if any(c.valor == 1 for c in jugador) and vj < 12:
            return Estrategia.MATA[vj - 3][vc - 1]
        return Estrategia.MATN[vj - 4][vc - 1]


class Mazo(object):
    """ Clase que representa un mazo de cartas
    """
    NUM_BARAJAS = 2
    SEMILLA = 260

    def __init__(self, clase_carta, estrategia):
        """ Crea un mazo y le asocia una estrategia
        :param clase_carta: La clase que representa las cartas
        :param estrategia: La estrategia asociada
        """
        self.clase = clase_carta
        self.estrategia = estrategia
        self.cartas = []
        random.seed(Mazo.SEMILLA)

    def reparte(self):
        """ Reparte una carta del mazo
            Llama al método cuenta_carta de la estrategia asociada
        :return: Un objeto carta de la clase indicada en el constructor
        """
        if len(self.cartas) == 0:
            # Se ha acabado el mazo: crear uno nuevo
            inds = list(range(52)) * Mazo.NUM_BARAJAS
            random.shuffle(inds)
            self.cartas = [self.clase(i) for i in inds]
        c = self.cartas.pop()
        if self.estrategia is not None:
            # Se informa a la estrategia de la carta que se reparte
            self.estrategia.cuenta_carta(c)
        return c

class CartaBase:
    """ Clase base para representar una carta. """

    def __init__(self, ind):
        """ Crea una carta con un índice dado
        :param ind: Índice de la carta
        """
        self.ind = ind

    @property
    def valor(self) -> int:
        """ Retorna el valor de la carta.
        :return: Valor de la carta
        """
        return self.ind % 13 + 1

class Carta(CartaBase):
    """ Clase para representar una carta. Hereda de la clase CartaBase y 
        la expande con métodos para representarla de forma lujosa.
    """
    def __str__(self) -> str:
        """ Método para representar la carta de manera lujosa en la terminal.
            Utiliza caracteres Unicode para formar los bordes.
        :return: String con la representación de la carta
        """
        borde_arriba = "\u256D\u2500\u2500\u2500\u256E\n"
        lin_num = f"\u2502 {self.numero}\u2502\n"
        lin_palo = f"\u2502{self.palo}  \u2502\n"
        borde_abajo = "\u2570\u2500\u2500\u2500\u256F"
        return "".join([borde_arriba, lin_num, lin_palo, borde_abajo])
    
    @property
    def palo(self) -> str:
        """ Este método calcula el palo correspondiente a una carta 
            basándose en su índice dentro de la baraja (0-51).
            Definimos de manera arbitraria el orden de la baraja como:
            treboles -> picas -> diamantes -> corazones.
        :return: Carácter Unicode representando el palo de la carta.
        """
        palos = ["\u2663", "\u2660", "\u2666", "\u2665"]
        return palos[self.ind // 13]
    
    @property
    def numero(self) -> str:
        """ Método que calcula el número que corresponde a la carta basándose
            en su índice. El índice 0 corresponde al as ('A') y los índices 
            10, 11 y 12 a las figuras ('J', 'Q' y 'K').
            Asegura que sea un string de 2 caracteres para hacer más fácil la
            representación de la carta en la consola.
        :return: String correspondiente al número de la carta.
        """
        nums = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']
        return nums[self.ind % 13]

class Mano(object):
    """ Clase para representar manos
    """
    def __init__(self, nombre: str, apuesta: int, cartas: List[Carta]) -> None:
        """ Crea e inicializa la mano
        :param nombre: Nombre de la mano, usado para la representación en la terminal
        :param apuesta: Apuesta asociada a la mano (es importante que sea en euros o el código no funciona)
        :param cartas: Cartas que añadir a la mano al crearla
        """
        self.nombre = nombre
        self.apuesta = apuesta
        self.estado = "Abierta"
        self.cartas = []
        for carta in cartas:
            self.añadir_carta(carta)

    def __str__(self) -> str:
        """ Método para representar una mano en la terminal de forma lujosa.
        :return: String con la representación de la mano
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
        """ Método para añadir cartas a la mano. Se encarga de actualizar 
            el estado de la mano después de añadir la carta.
        """
        self.cartas += [carta]
        if self.valor > 21:
            self.estado = "PASADA"

    def cerrar(self):
        """ Método para cerrar la mano.
        """
        self.estado = "Cerrada"

    def doblar(self, carta: Carta):
        """ Método para doblar la mano. Dobla la apuesta, cierra la mano 
            y añade una carta.
        """
        self.apuesta = self.apuesta * 2
        self.cerrar()
        self.añadir_carta(carta)

    def separar(self) -> List[Self]:
        """ Método para separar la mano. Solo puede ser llamado si la mano tiene 
            exactamente dos cartas con el mismo valor numérico. Separa la mano
            en dos, con una carta cada una.
        :return: Lista con las dos manos separadas
        """
        return [Mano(self.nombre + l, apuesta=self.apuesta, cartas=[c]) for c, l in zip(self.cartas, ["A", "B"])]
    
    def opciones(self) -> Dict[str, str]:
        """ Método para calcular las opciones disponibles para la mano. Las posibles
            opciones son: pedir otra carta (P), cerrar la mano (C), doblar la apuesta (D),
            o separar la mano en dos. Esta última solo está disponible si la mano tiene 
            únicamente dos cartas con el mismo valor numérico.
        :return: Diccionario con las posibles opciones
        """
        if self.estado in ["PASADA", "Cerrada"]:
            return []
        opcs = {"p": "[P]edir", "c": "[C]errar", "d": "[D]oblar"}
        if len(self.cartas) == 2 and self.cartas[0].valor == self.cartas[1].valor:
            opcs["s"] = "[S]eparar"
        return opcs

def unir_str_por_linea(a, b):
    """ Función de ayuda para unir dos strings con un salto de línea en el medio. """
    return f"{a}\n{b}"


def jugar_partida(mazo: Mazo, estrategia: Estrategia, balance: int, num_part: int):
    """Función para jugar una partida de blackjack."""
    print(F"--- INICIO DE LA PARTIDA #{num_part} --- BALANCE = {balance} €")
    apuesta = input("¿Apuesta? [2] [10] [50]: ")
    while apuesta not in ["2", "10", "50", ""]:
        apuesta = input("¿Apuesta? [2] [10] [50]: ")
    apuesta = 10 if apuesta == "" else int(apuesta)

    print("\nREPARTO INICIAL")
    mano_cr = Mano("Croupier", apuesta, cartas=[mazo.reparte()])
    mano_jug = Mano("Mano", apuesta, cartas=[mazo.reparte(), mazo.reparte()])
    print(str(mano_cr))
    print(str(mano_jug))

    if mano_jug.valor == 21:
        output = apuesta * (3/2)
        print("*****************\n*** BLACKJACK ***\n*****************\n")
        print(f"Ha ganado {output} €!")
        return output


def main():
    estrategia = Estrategia(Mazo.NUM_BARAJAS)
    mazo = Mazo(Carta, estrategia)
    balance = 0

    print("*** BLACKJACK - PARADIGMAS DE PROGRAMACIÓN 2023/24 ***")
    modo = input("¿Modo de ejecución? [J]uego [A]nálisis: ")
    while modo.lower() not in ["j", "a", ""]:
        modo = input("¿Modo de ejecución? [J]uego [A]nálisis: ")

    # modo Juego se ejecuta por defecto si el usuario le da a enter
    if modo.lower() in ["j", ""]:
        num_part = 1
        otra = "s"
        while otra.lower() in ["s", ""]:
            balance += jugar_partida(mazo, estrategia, balance, num_part)
            otra = input("¿Otra partida? [S/N]: ")
            while otra.lower() not in ["s", "n", ""]:
                otra = input("¿Otra partida? [S/N]: ")
        print(f"BALANCE FINAL: {balance} €")


if __name__ == "__main__":
    main()
