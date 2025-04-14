from othello import (
    Ficha,
    Othello,
    # pretty_print_othello,
    pretty_print_othello_con_jugadas_legales,
)

if __name__ == "__main__":
    juego = Othello()
    s = juego.inicializa()
    tablero = s[0]
    jugador = s[1]
    while True:
        pretty_print_othello_con_jugadas_legales(tablero, juego, jugador)
        print(f"Turno de {Ficha(jugador).name}")
        x = int(input("Fila: "))
        y = int(input("Col: "))
        tablero = juego.transicion(tablero, (x, y), jugador)
        jugador *= -1
