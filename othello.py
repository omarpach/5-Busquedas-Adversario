"""
Juego de Othello

El estado se va a representar como una matriz de 8x8

Ficha negra = 1
Ficha blanca = -1
Espacio vacio = 0

Jugador 1 = negro
Jugador 2 = blanco

"""

import numpy as np
from juegos_simplificado import ModeloJuegoZT2
from enum import IntEnum, Enum


class Ficha(IntEnum):
    NEGRA = 1
    BLANCA = -1
    VACIA = 0


class Direccion(Enum):
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SO = (1, -1)
    O = (0, -1)
    NO = (-1, -1)


class Othello(ModeloJuegoZT2):
    def inicializa(self):
        s0: np.ndarray = np.zeros((8, 8), dtype=np.int8)
        s0[3][4] = Ficha.NEGRA
        s0[4][3] = Ficha.NEGRA
        s0[3][3] = Ficha.BLANCA
        s0[4][4] = Ficha.BLANCA
        return (s0, 1)

    def jugadas_legales(self, s, j):
        fichas_oponentes = buscar_fichas(s, j * -1)
        print(fichas_oponentes)
        posibles_jugadas_legales = set()
        jugadas_legales = []
        for ficha in fichas_oponentes:
            posibles_jugadas = buscar_fichas_vecinas(s, ficha, Ficha.VACIA)
            for posible_jugada in posibles_jugadas:
                posibles_jugadas_legales.add(posible_jugada)
        for p in posibles_jugadas_legales:
            if es_legal(s, j, p):
                jugadas_legales.append(p)
        # p = posibles_jugadas_legales.pop()
        # if es_legal(s, j, p):
        #     return p
        return jugadas_legales

    """
    Checa si hay casillas vacias, si hay una casilla vacia
    el juego no ha acabado.
    TODO: si hay solo fichas blancas o negras el juego acaba
    """

    def terminal(self, s):
        iter = s.flat
        for x in iter:
            if x == Ficha.VACIA:
                return False
        return True

    def ganancia(self, s):
        iter = s.flat
        sum_fichas_j1 = 0
        for x in iter:
            if x == Ficha.NEGRA:
                sum_fichas_j1 += 1
        return sum_fichas_j1


def buscar_fichas(s, tipo_ficha: int):
    fichas = []
    for i in range(8):
        for j in range(8):
            if s[i][j] == tipo_ficha:
                fichas.append((i, j))
    return fichas


def buscar_fichas_vecinas(
    s, pos_ficha: tuple[int, int], tipo_ficha: int
) -> list[tuple[int, int]]:
    fichas_vecinas = []
    x, y = pos_ficha
    inicio = 1 if y == 0 else 0
    final = 2 if y == 7 else 3
    for i in range(inicio, final):
        if x != 0:
            if s[x - 1][y - 1 + i] == tipo_ficha:
                fichas_vecinas.append((x - 1, y - 1 + i))
        if s[x][y - 1 + i] == tipo_ficha and i != 1:
            fichas_vecinas.append((x, y - 1 + i))
        if x != 7:
            if s[x + 1][y - 1 + i] == tipo_ficha:
                fichas_vecinas.append((x + 1, y - 1 + i))
    return fichas_vecinas


def calcular_direccion(ficha1: tuple[int, int], ficha2: tuple[int, int]) -> Direccion:
    x1, y1 = ficha1
    x2, y2 = ficha2
    dx, dy = x2 - x1, y2 - y1
    return Direccion((dx, dy))


def avanzar_direccion(ficha: tuple[int, int], dir: Direccion) -> tuple[int, int]:
    x, y = ficha
    dx, dy = dir.value
    return (x + dx, y + dy)


def es_legal(s, j: int, p: tuple[int, int]) -> bool:
    vecinos_oponentes = buscar_fichas_vecinas(s, p, j * -1)
    es_legal = False
    for v in vecinos_oponentes:
        if not es_legal:
            dir = calcular_direccion(p, v)
            continuar = True
            aux = p
            while continuar:
                nueva_pos = avanzar_direccion(aux, dir)
                x, y = nueva_pos
                if x < 0 or x > 7 or y < 0 or y > 7:
                    continuar = False
                if s[x][y] == j:
                    es_legal = True
                    continuar = False
                elif s[x][y] == Ficha.VACIA:
                    continuar = False
                aux = nueva_pos
    return es_legal


def pretty_print_othello(s):
    print("\n   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
    separador_filas = "+---" * 8
    separador_filas = "---" + separador_filas + "+"
    print(separador_filas)
    for i in range(8):
        fila = s[i]
        valores_fila = [
            " X "
            if int(x) == Ficha.NEGRA
            else " O "
            if int(x) == Ficha.BLANCA
            else "   "
            for x in fila
        ]
        num_fila = f" {i} |"
        pretty_fila = num_fila + "|".join(valores_fila) + "|"
        print(pretty_fila)
        print(separador_filas)


def pretty_print_othello_debug(s):
    print("\n   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
    separador_filas = "+---" * 8
    separador_filas = "---" + separador_filas + "+"
    print(separador_filas)
    for i in range(8):
        fila = s[i]
        valores_fila = [
            " X "
            if int(x) == Ficha.NEGRA
            else " O "
            if int(x) == Ficha.BLANCA
            else " - "
            if int(x) == 2
            else "   "
            for x in fila
        ]
        num_fila = f" {i} |"
        pretty_fila = num_fila + "|".join(valores_fila) + "|"
        print(pretty_fila)
        print(separador_filas)
