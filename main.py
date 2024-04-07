from externo import Mazo, Estrategia
from carta import Carta
from mano import Mano
from otros import unir_str_por_linea
from functools import reduce


def jugar_manos(mazo, manos_jug):
    for i, mano in enumerate(manos_jug):
        manos_jug_copia = manos_jug.copy()
        opciones_mano = mano.opciones()
        if not opciones_mano:
            continue
        opcs_output = f"¿Jugada para {mano.nombre}? {' '.join(opciones_mano.values())} "
        opcion = input(opcs_output)
        while opcion.lower() not in opciones_mano.keys():
            opcion = input(opcs_output)

        if opcion.lower() == "p":
            mano.añadir_carta(mazo.reparte())
        elif opcion.lower() == "c":
            mano.cerrar()
        elif opcion.lower() == "d":
            mano.doblar(mazo.reparte())
        elif opcion.lower() == "s":
            manos_jug_copia.pop(i)
            manos_jug_copia.extend(mano.separar())
    return manos_jug_copia


def jugar_partida(mazo: Mazo, estrategia: Estrategia, balance: int, num_part: int):
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
    
    manos_jug = [mano_jug]
    manos_jug = jugar_manos(mazo, manos_jug)
    while len([m for m in manos_jug if m.estado == "Abierta"]) > 0:
        repr_manos = []
        for mano in manos_jug[:-1]:
            repr_manos.append(unir_str_por_linea(str(mano), " | \n | \n | \n | "))
        repr_manos.append(str(manos_jug[-1]))
        print(reduce(unir_str_por_linea, repr_manos))
        manos_jug = jugar_manos(mazo, manos_jug)
        

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