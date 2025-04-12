from othello import Othello, pretty_print_othello
import numpy as np

if __name__ == "__main__":
    juego = Othello()
    s = juego.inicializa()
    matriz = s[0]
    print(juego.terminal(s))
    pretty_print_othello(s)
