from externo import Mazo, Estrategia
from carta import Carta
from mano import Mano
from otros import unir_str_por_linea
from functools import reduce
from typing import List


def reparto_inicial(mazo, apuesta):
    print("\nREPARTO INICIAL")
    mano_cr = Mano("Croupier", apuesta, cartas=[mazo.reparte()])
    mano_jug = Mano("Mano", apuesta, cartas=[mazo.reparte(), mazo.reparte()])
    print(str(mano_cr))
    print(str(mano_jug))
    return mano_cr, mano_jug, mazo


def check_blackjack(apuesta, mano_jug):
    if mano_jug.valor == 21:
        output = int(apuesta * (3/2))
        print("*****************\n*** BLACKJACK ***\n*****************\n")
        print(f"Ha ganado {output} €!")
        return output
    else:
        return False
    

def jugar_opcion(mazo, manos_jug_copia, manos_separadas, i, mano, jugada):
    if jugada.lower() == "p":
        mano.añadir_carta(mazo.reparte())
    elif jugada.lower() == "c":
        mano.cerrar()
    elif jugada.lower() == "d":
        mano.doblar(mazo.reparte())
    elif jugada.lower() == "s":
        manos_jug_copia.pop(i - len(manos_separadas)//2)
        manos_separadas.extend(mano.separar())
    return mazo, manos_jug_copia, manos_separadas
    

def jugar_manos(mazo, manos_jug):
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


def representar_manos(manos_jug):
    repr_manos = [unir_str_por_linea(str(m), " | \n | \n | \n | ") for m in manos_jug[:-1]] + [str(manos_jug[-1])]
    return reduce(unir_str_por_linea, repr_manos)


def jugar_turno_croupier(mazo, mano_cr):
    print("\nTURNO DEL CROUPIER")
    print(str(mano_cr))
    while mano_cr.valor < 17:
        mano_cr.añadir_carta(mazo.reparte())
        print(str(mano_cr))
    return mazo, mano_cr


def contabilizar_resultados(mano_cr, manos_jug):
    print("\nCONTABILIZACIÓN DE RESULTADOS")
    for mano in manos_jug:
        print(f"* Croupier: {mano_cr.valor}, {mano.nombre}: {mano.valor} -> {mano.evaluar(mano_cr) * mano.apuesta}")
    res = sum([m.evaluar(mano_cr) * m.apuesta for m in manos_jug])
    print(f"Resultado de la partida: {'+' if res >= 0 else '-'}{abs(res)}")
    return res


def jugar_partida(mazo: Mazo, balance: int, num_part: int):
    print(f"\n--- INICIO DE LA PARTIDA #{num_part} --- BALANCE = {balance} €")
    apuesta = input("¿Apuesta? [2] [10] [50]: ")
    while apuesta not in ["2", "10", "50", ""]:
        apuesta = input("¿Apuesta? [2] [10] [50]: ")
    apuesta = 10 if apuesta == "" else int(apuesta)

    mano_cr, mano_jug, mazo = reparto_inicial(mazo, apuesta)
    print(str(mano_cr))
    print(str(mano_jug))
    blackjack = check_blackjack(apuesta, mano_jug)
    if blackjack: 
        return mazo, blackjack

    print("\nTURNO DEL JUGADOR")
    manos_jug = [mano_jug]
    while len([m for m in manos_jug if m.estado == "Abierta"]) > 0:
        mazo, manos_jug = jugar_manos(mazo, manos_jug)
        print("\n" + representar_manos(manos_jug))
    
    if len([m for m in manos_jug if m.estado == "PASADA"]) != len(manos_jug):    
        mazo, mano_cr = jugar_turno_croupier(mazo, mano_cr)

    print("\nFIN DE PARTIDA")
    print(str(mano_cr))
    print(representar_manos(manos_jug))
    res = contabilizar_resultados(mano_cr, manos_jug)
    return mazo, res


def analizar_partida(mazo: Mazo, estrategia: Estrategia, balance: int, num_part: int):
    print(f"\n--- INICIO DE LA PARTIDA #{num_part} --- BALANCE = {balance} €")
    apuesta = estrategia.apuesta(2, 10, 50)
    print(f"¿Apuesta? [2] [10] [50]: {apuesta}")

    mano_cr, mano_jug, mazo = reparto_inicial(mazo, apuesta)
    blackjack = check_blackjack(apuesta, mano_jug)
    if blackjack: 
        return mazo, estrategia, blackjack

    print("\nTURNO DEL JUGADOR")
    manos_jug = [mano_jug]
    while len([m for m in manos_jug if m.estado == "Abierta"]) > 0:
        mazo, estrategia, manos_jug = analizar_manos(mazo, estrategia, manos_jug, mano_cr)
        print("\n" + representar_manos(manos_jug))

    if len([m for m in manos_jug if m.estado == "PASADA"]) != len(manos_jug): 
        mazo, mano_cr = jugar_turno_croupier(mazo, mano_cr)
        
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
                break
            except ValueError: 
                num_partidas = input("¿Número de partidas? ")
        for i in range(num_partidas):
            mazo, estrategia, res = analizar_partida(mazo, estrategia, balance, i+1)
            balance += res

    print(f"\nBALANCE FINAL: {balance} €")


if __name__ == "__main__":
    main()