from externo import Mazo, Estrategia
from carta import Carta
from mano import Mano


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
    print(str(mano))

    if mano.valor == 21:
        output = apuesta * (3/2)
        print("*****************\n*** BLACKJACK ***\n*****************\n")
        print(f"Ha ganado {output} €!")
        return output
    
    manos_jug = [mano_jug]
    while len([m for m in manos_jug if m.estado == "Abierta"]) > 0:
        for i, mano in enumerate(manos_jug): 

            opciones_mano = mano.opciones()
            if not opciones_mano:
                continue
            opcion = input(f"¿Jugada para {mano.nombre}? {" ".join(opciones_mano.values())}")
            while opcion.lower() not in opciones_mano.keys():
                opcion = input(f"¿Jugada para {mano.nombre}? {" ".join(opciones_mano.values())}")

            if opcion.lower() == "p":
                mano.añadir_carta(mazo.reparte())
            elif opcion.lower() == "c":
                mano.cerrar()
            elif opcion.lower() == "d":
                mano.doblar()
            elif opcion.lower() == "s":
                manos_jug.pop(i)
                manos_jug.extend(mano.separar())
        

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