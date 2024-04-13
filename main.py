from externo import Mazo, Estrategia
from carta import Carta
from mano import Mano
from otros import unir_str_por_linea
from functools import reduce


def jugar_manos(mazo, manos_jug):
    # Para no iterar y modificar la misma lista a la vez, 
    # creamos una copia de la lista que contiene las manos.
    manos_jug_copia = manos_jug.copy()
    manos_separadas = 0
    for i, mano in enumerate(manos_jug):
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
            # Al separar una  mano, borramos la mano original de la lista, 
            # por lo que el indice de las siguientes manos se reduce por uno. 
            # Por tanto, hay que reducir el indice de la mano que vamos a eliminar 
            # el numero de veces que hayamos separado una mano.
            manos_jug_copia.pop(i - manos_separadas)
            manos_jug_copia.extend(mano.separar())
            manos_separadas += 1
    return manos_jug_copia


def representar_manos(manos_jug):
    repr_manos = []
    for mano in manos_jug[:-1]:
        repr_manos.append(unir_str_por_linea(str(mano), " | \n | \n | \n | "))
    repr_manos.append(str(manos_jug[-1]))
    return reduce(unir_str_por_linea, repr_manos)


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
    
    print("\nTURNO DEL JUGADOR")

    manos_jug = [mano_jug]
    manos_jug = jugar_manos(mazo, manos_jug)
    while len([m for m in manos_jug if m.estado == "Abierta"]) > 0:
        print(f"\n{representar_manos(manos_jug)}")
        manos_jug = jugar_manos(mazo, manos_jug)
    
    print(f"\n{representar_manos(manos_jug)}")

    print("\nTURNO DEL CROUPIER")
    print(str(mano_cr))
    if len([m for m in manos_jug if m.estado == "Cerrada"]) > 0:
        while mano_cr.valor < 17:
            mano_cr.añadir_carta(mazo.reparte())
            print(f"\n{str(mano_cr)}")
        if mano_cr.estado != "PASADA" and mano_cr.valor >= 17:
            mano_cr.cerrar()

    print("\nFIN DE LA PARTIDA")
    print(f"{mano_cr}")
    print(f"{representar_manos(manos_jug)}")
    print("\nCONTABILIZACION DE RESULTADOS")

    resultado = 0
    for mano_jug in manos_jug:
        comparar = mano_jug.evaluar(mano_cr)
        print(f"* Croupier: {mano_cr.valor}, {mano_jug.nombre}: {mano_jug.valor} -> {'+' if comparar >= 0 else '-'}{abs(comparar)}")
        resultado += comparar
    print(f"Resultado de la partida: {'+' if resultado >= 0 else '-'}{abs(resultado)}")
    return resultado

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
            num_part += 1
            while otra.lower() not in ["s", "n", ""]:
                otra = input("¿Otra partida? [S/N]: ")
        print(f"BALANCE FINAL: {balance} €")



if __name__ == "__main__":
    main()