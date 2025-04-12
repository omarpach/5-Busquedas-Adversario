"""
Juego de Othello

El estado se va a representar como una matriz de 8x8

Ficha negra = 1
Ficha blanca = -1
Espacio vacio = 0

"""

import numpy as np
from juegos_simplificado import ModeloJuegoZT2


class Othello(ModeloJuegoZT2):
    def inicializa(self):
        s0: np.ndarray = np.zeros((8, 8), dtype=np.int8)
        s0[3][4] = 1
        s0[4][3] = 1
        s0[3][3] = -1
        s0[4][4] = -1
        return (s0, 1)

    """
    Checa si hay casillas vacias, si hay una casilla vacia
    el juego no ha acabado.
    """

    def terminal(self, s):
        matriz = s[0]
        iter = matriz.flat
        for x in iter:
            if x == 0:
                return False
        return True


def pretty_print_othello(s):
    print("\n   | A | B | C | D | E | F | G | H |")
    separador_filas = "+---" * 8
    separador_filas = "---" + separador_filas + "+"
    matriz_juego = s[0]
    print(separador_filas)
    for i in range(1, 9):
        fila = matriz_juego[i - 1]
        valores_fila = [
            " X " if int(x) == 1 else " O " if int(x) == -1 else "   " for x in fila
        ]
        num_fila = f" {i} |"
        pretty_fila = num_fila + "|".join(valores_fila) + "|"
        print(pretty_fila)
        print(separador_filas)
