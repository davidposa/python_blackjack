from externo import Mazo, Estrategia
from carta import Carta
from mano import Mano
from otros import unir_str_por_linea
from functools import reduce
from typing import List
from time import sleep
from sys import stdout


def reparto_inicial(mazo: Mazo, apuesta: int):
    """ Funcion que se encarga de repartir la mano inicial al jugador
    y al croupier. 
    :param mazo: objeto de la clase Mazo del cual repartir las cartas
    :param apuesta: cantidad apostada por el jugador
    :return: tupla conteniendo la mano del croupier, la del jugador, y el mazo
    """
    print("\nREPARTO INICIAL")
    mano_cr = Mano("Croupier", apuesta, cartas=[mazo.reparte()])
    mano_jug = Mano("Mano", apuesta, cartas=[mazo.reparte(), mazo.reparte()])
    print(str(mano_cr))
    print(str(mano_jug))
    return mano_cr, mano_jug, mazo


def hay_blackjack(apuesta: int, mano_jug: Mano, modo: str="j"):
    """ Funcion que se encarga de comprobar si hay blackjack en la primera ronda
        de cada partida. Devuelve la apuesta ganada si la mano vale 21 puntos, y
        False en caso contrario.
    :param apuesta: cantidad apostada por el jugador
    :param mano_jug: objeto de la clase Mano con la mano del jugador
    :param modo: string que determina si la partida es en modo juego o en modo
    analisis. En modo juego imprime el mensaje de blackjack a la terminal letra por
    letra, y en modo analisis lo imprime todo a la vez.
    :return: la apuesta ganada si hay blackjack, False en caso contrario
    """
    blackjack_str = "*****************\n*** BLACKJACK ***\n*****************\n"
    if mano_jug.valor == 21:
        output = int(apuesta * (3/2))
        if modo == "j":
            for letra in blackjack_str:
                print(letra, end="")
                # se necesita para imprimir letra por letra en vez de linea por linea
                stdout.flush()
                sleep(0.00001)
            print("\n")
        else:
            print(blackjack_str)
        print(f"Ha ganado {output} €!")
        return output
    else:
        return False
    

def jugar_opcion(
        mazo: Mazo,
        manos_jug: List[Mano],
        manos_separadas:List[Mano],
        mano: Mano,
        i: int,
        opcion: str
    ):
    """ Funcion para aplicar la opcion escogida por el jugador a cada mano.
    :param mazo: objeto de la clase Mazo del cual repartir cartas
    :param manos_jug: lista con las manos del jugador
    :param manos_separadas: lista con manos que el jugador ha separado este turno
    :param mano: mano a la cual aplicar la opcion
    :param i: indice de la mano dentro de la lista manos_jug
    :param opcion: opcion escogida por el jugador 
    :return: tupla conteniendo el mazo, la lista con las manos del jugador, y la
    lista con las manos separadas por el jugador
    """
    if opcion.lower() == "p":
        mano.añadir_carta(mazo.reparte())
    elif opcion.lower() == "c":
        mano.cerrar()
    elif opcion.lower() == "d":
        mano.doblar(mazo.reparte())
    elif opcion.lower() == "s":
        # por cada mano separada (dos manos creadas) el indice de las siguientes manos dentro
        # de manos_jug se reduce por 1
        manos_jug.pop(i - len(manos_separadas)//2)
        manos_separadas.extend(mano.separar())
    return mazo, manos_jug, manos_separadas
    

def jugar_manos(mazo: Mazo, manos_jug: List[Mano]):
    """ Funcion para jugar todas las manos del jugador en una ronda de la partida en modo juego.
    :param mazo: objeto de la clase Mazo del cual repartir cartas
    :param manos_jug: lista con las manos del jugador
    :return: tupla con el mazo y las manos del jugador tras la ronda
    """
    # copiamos la lista para no modificar la misma por la cual estamos iterando
    manos_jug_copia = manos_jug.copy()
    manos_separadas = []
    for i, mano in enumerate(manos_jug):
        opciones_mano = mano.opciones
        if not opciones_mano:
            continue
        opcs_output = f"¿Jugada para {mano.nombre}? {' '.join(opciones_mano.values())} "
        opcion = input(opcs_output)
        while opcion.lower() not in opciones_mano.keys():
            opcion = input(opcs_output)
        mazo, manos_jug_copia, manos_separadas = jugar_opcion(mazo, manos_jug_copia, manos_separadas, i, mano, opcion)
    return mazo, manos_jug_copia + manos_separadas


def analizar_manos(mazo: Mazo, estrategia: Estrategia, manos_jug: List[Mano], mano_cr: Mano):
    """ Funcion para jugar todas las manos del jugador en una ronda de la partida en modo analisis.
    :param mazo: objeto de la clase Mazo del cual repartir cartas
    :param estrategia: objeto de la clase Estrategia que predice la jugada para cada mano
    :param manos_jug: lista con las manos del jugador
    :param mano_cr: objeto de la clase Mano con la mano del croupier
    :return: tupla con el mazo, la estrategia, y las manos del jugador tras la ronda
    """
    # copiamos la lista para no modificar la misma por la cual estamos iterando
    manos_jug_copia = manos_jug.copy()
    manos_separadas = []
    for i, mano in enumerate(manos_jug):
        opciones_mano = mano.opciones
        if not opciones_mano:
            continue
        jugada = estrategia.jugada(*mano_cr.cartas, mano.cartas)
        print(f"¿Jugada para {mano.nombre}? {' '.join(opciones_mano.values())} {jugada}")
        mazo, manos_jug_copia, manos_separadas = jugar_opcion(mazo, manos_jug_copia, manos_separadas, i, mano, jugada)
    return mazo, estrategia, manos_jug_copia + manos_separadas


def representar_manos(manos_jug: List[Mano]):
    """ Funcion para representar todas las manos del jugador.
    :param manos_jug: lista con las manos del jugador
    :return: string con la representacion de las manos
    """
    repr_manos = [unir_str_por_linea(str(m), " | \n | \n | \n | ") for m in manos_jug[:-1]] + [str(manos_jug[-1])]
    return reduce(unir_str_por_linea, repr_manos)


def jugar_turno_croupier(mazo: Mazo, mano_cr: Mano, modo: str="j"):
    """ Funcion para jugar el turno del croupier. El croupier pide cartas hasta que el valor
        de su mano iguala o supera 17.
    :param mazo: objeto de la clase Mazo del cual repartir cartas
    :param mano_cr: objeto de la clase Mano con la mano del croupier
    :param modo: string que determina si la partida es en modo juego o en modo analisis. En 
    modo juego pausa brevemente antes de repartir cada carta.
    :return: tupla con el mazo y la mano del croupier
    """
    print("\nTURNO DEL CROUPIER")
    print(str(mano_cr))
    sleep_time = 0.75
    while mano_cr.valor < 17:
        if modo == "j":
            sleep(sleep_time)
        mano_cr.añadir_carta(mazo.reparte())
        print(str(mano_cr))
        sleep_time += 0.25
    if modo == "j":
        sleep(0.75)
    return mazo, mano_cr


def contabilizar_resultados(mano_cr: Mano, manos_jug: List[Mano]) -> int:
    """ Funcion para contabilizar los resultados al final de una partida.
    :param mano_cr: objeto de la clase Mano con la mano del croupier
    :param manos_jug: lista con las manos del jugador
    :return: cantidad ganada (o perdida) por el jugador al final de la partida
    """
    print("\nCONTABILIZACIÓN DE RESULTADOS")
    for mano in manos_jug:
        print(f"* Croupier: {mano_cr.valor}, {mano.nombre}: {mano.valor} -> {mano.evaluar(mano_cr) * mano.apuesta}")
    res = sum([m.evaluar(mano_cr) * m.apuesta for m in manos_jug])
    print(f"Resultado de la partida: {'+' if res >= 0 else '-'}{abs(res)}")
    return res


def jugar_partida(mazo: Mazo, balance: int, num_part: int):
    """ Funcion para jugar una partida completa en modo juego.
    :param mazo: objeto de la clase Mazo del cual repartir cartas
    :param balance: balance del jugador al inicio de la partida
    :num_part: numero de la partida dentro de una ejecucion del programa
    :return: tupla con el mazo y la cantidad ganada (o perdida) al final de la partida
    """
    print(f"\n--- INICIO DE LA PARTIDA #{num_part} --- BALANCE = {balance} €")
    apuesta = input("¿Apuesta? [2] [10] [50]: ")
    while apuesta not in ["2", "10", "50", ""]:
        apuesta = input("¿Apuesta? [2] [10] [50]: ")
    apuesta = 10 if apuesta == "" else int(apuesta)

    mano_cr, mano_jug, mazo = reparto_inicial(mazo, apuesta)
    blackjack = hay_blackjack(apuesta, mano_jug)
    if blackjack: 
        return mazo, blackjack

    print("\nTURNO DEL JUGADOR")
    manos_jug = [mano_jug]
    while len([m for m in manos_jug if m.estado == "Abierta"]) > 0:
        mazo, manos_jug = jugar_manos(mazo, manos_jug)
        print("\n" + representar_manos(manos_jug))
    
    # el croupier solo pide cartas si el jugador no se ha pasado en todas sus manos
    if len([m for m in manos_jug if m.estado == "PASADA"]) != len(manos_jug):    
        mazo, mano_cr = jugar_turno_croupier(mazo, mano_cr)

    print("\nFIN DE PARTIDA")
    print(str(mano_cr))
    print(representar_manos(manos_jug))
    res = contabilizar_resultados(mano_cr, manos_jug)
    return mazo, res


def analizar_partida(mazo: Mazo, estrategia: Estrategia, balance: int, num_part: int):
    """ Funcion para jugar una partida completa en modo analisis.
    :param mazo: objeto de la clase Mazo del cual repartir cartas
    :param estrategia: objeto de la clase Estrategia usado para predecir la apuesta inicial y la
    jugada para cada mano.
    :param balance: balance del jugador al inicio de la partida
    :num_part: numero de la partida dentro de una ejecucion del programa
    :return: tupla con el mazo, la estrategia, y la cantidad ganada (o perdida) al final de la partida
    """
    print(f"\n--- INICIO DE LA PARTIDA #{num_part} --- BALANCE = {balance} €")
    apuesta = estrategia.apuesta(2, 10, 50)
    print(f"¿Apuesta? [2] [10] [50]: {apuesta}")

    mano_cr, mano_jug, mazo = reparto_inicial(mazo, apuesta)
    blackjack = hay_blackjack(apuesta, mano_jug, modo="a")
    if blackjack: 
        return mazo, estrategia, blackjack

    print("\nTURNO DEL JUGADOR")
    manos_jug = [mano_jug]
    while len([m for m in manos_jug if m.estado == "Abierta"]) > 0:
        mazo, estrategia, manos_jug = analizar_manos(mazo, estrategia, manos_jug, mano_cr)
        print("\n" + representar_manos(manos_jug))
    
    # el croupier solo pide cartas si el jugador no se ha pasado en todas sus manos
    if len([m for m in manos_jug if m.estado == "PASADA"]) != len(manos_jug): 
        mazo, mano_cr = jugar_turno_croupier(mazo, mano_cr, modo="a")
        
    print("\nFIN DE PARTIDA")
    print(str(mano_cr))
    print(representar_manos(manos_jug))
    res = contabilizar_resultados(mano_cr, manos_jug)
    return mazo, estrategia, res


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
            mazo, res = jugar_partida(mazo, balance, num_part)
            balance += res
            num_part += 1
            otra = input("¿Otra partida? [S/N]: ")
            while otra.lower() not in ["s", "n", ""]:
                otra = input("¿Otra partida? [S/N]: ")

    elif modo.lower() == "a":
        num_partidas = input("¿Número de partidas? ")
        while True:
            try: 
                num_partidas = int(num_partidas)
                assert num_partidas > 0
                break
            except (ValueError, AssertionError): 
                num_partidas = input("¿Número de partidas? ")
        for i in range(num_partidas):
            mazo, estrategia, res = analizar_partida(mazo, estrategia, balance, i+1)
            balance += res

    print(f"\nBALANCE FINAL: {balance} €")


if __name__ == "__main__":
    main()