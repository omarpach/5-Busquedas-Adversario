from othello import (
    Ficha,
    Othello,
    pretty_print_othello,
    pretty_print_othello_debug,
)

if __name__ == "__main__":
    juego = Othello()
    print("X = ficha negra\nO = ficha blanca")
    s = juego.inicializa()
    s0 = s[0]
    pretty_print_othello(s0)
    print("Jugadas legales para NEGRA")
    s1 = s0.copy()
    jugadas_legales = juego.jugadas_legales(s0, Ficha.NEGRA)
    for j in jugadas_legales:
        s1[j[0], j[1]] = 2
    pretty_print_othello_debug(s1)
    # print(juego.jugadas_legales(s0, Ficha.NEGRA))
