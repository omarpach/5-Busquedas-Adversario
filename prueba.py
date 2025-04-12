from othello import Othello, pretty_print_othello

if __name__ == "__main__":
    juego = Othello()
    s = juego.inicializa()
    fila = s[0][0]
    # print(type(fila))
    # print(fila)
    pretty_print_othello(s)
