from externo import Mazo, Estrategia
from carta import Carta


def main():
    estrategia = Estrategia(Mazo.NUM_BARAJAS)
    mazo = Mazo(Carta, estrategia)


if __name__ == "__main__":
    main()