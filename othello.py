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
from juegos_simplificado import ModeloJuegoZT2, juega_dos_jugadores
from enum import IntEnum, Enum
from minimax import minimax_iterativo, jugador_negamax


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

    def jugadas_legales(self, s: np.ndarray, j):
        fichas_oponentes = buscar_fichas(s, j * -1)
        posibles_jugadas_legales = set()
        jugadas_legales = []
        for ficha in fichas_oponentes:
            posibles_jugadas = buscar_fichas_vecinas(s, ficha, Ficha.VACIA)
            for posible_jugada in posibles_jugadas:
                posibles_jugadas_legales.add(posible_jugada)
        for p in posibles_jugadas_legales:
            if es_legal(s, j, p):
                jugadas_legales.append(p)
        return jugadas_legales

    def transicion(self, s, a, j):
        nuevo_estado = s.copy()
        direcciones = [
            calcular_direccion(a, v) for v in buscar_fichas_vecinas(s, a, j * -1)
        ]
        for d in direcciones:
            ficha_propia = buscar_ficha_en_dir(s, a, d, j)
            if ficha_propia is not None:
                voltear_fichas_en_rango(nuevo_estado, a, ficha_propia, d)
        if nuevo_estado[a[0]][a[1]] == Ficha.VACIA:
            nuevo_estado[a[0]][a[1]] = j
        return nuevo_estado

    """
    Checa si hay casillas vacias, si hay una casilla vacia
    el juego no ha acabado.
    """

    def terminal(self, s):
        iter = s.flat
        hay_casillas_vacias = False
        hay_fichas_blancas = False
        hay_fichas_negras = False
        for x in iter:
            if x == Ficha.VACIA:
                hay_casillas_vacias = True
            elif x == Ficha.BLANCA:
                hay_fichas_blancas = True
            else:
                hay_fichas_negras = True
        return not (hay_fichas_blancas and hay_fichas_negras and hay_casillas_vacias)

    def ganancia(self, s):
        iter = s.flat
        sum_negras = 0
        sum_blancas = 0
        for x in iter:
            if x == Ficha.NEGRA:
                sum_negras += 1
            elif x == Ficha.BLANCA:
                sum_blancas += 1
        if sum_negras > sum_blancas:
            return Ficha.NEGRA.value
        elif sum_blancas > sum_negras:
            return Ficha.BLANCA.value
        else:
            return Ficha.VACIA.value


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
                if esta_en_rango(nueva_pos):
                    x, y = nueva_pos
                    if s[x][y] == j:
                        es_legal = True
                        continuar = False
                    elif s[x][y] == Ficha.VACIA:
                        continuar = False
                    aux = nueva_pos
                else:
                    continuar = False
    return es_legal


def buscar_ficha_en_dir(
    s, ficha_inicial: tuple[int, int], dir: Direccion, tipo_ficha: Ficha
) -> tuple[int, int] | None:
    seguir_buscando = True
    ficha_actual = avanzar_direccion(ficha_inicial, dir)
    while seguir_buscando:
        if not esta_en_rango(ficha_actual):
            return None
        valor_ficha = s[ficha_actual[0]][ficha_actual[1]]
        if valor_ficha == Ficha.VACIA:
            return None
        elif valor_ficha == tipo_ficha:
            return ficha_actual
        ficha_actual = avanzar_direccion(ficha_actual, dir)


def voltear_fichas_en_rango(
    s, ficha_inicial: tuple[int, int], ficha_final: tuple[int, int], dir: Direccion
):
    ficha_actual = avanzar_direccion(ficha_inicial, dir)
    while ficha_actual != ficha_final:
        i, j = ficha_actual
        s[i][j] *= -1
        ficha_actual = avanzar_direccion(ficha_actual, dir)


def esta_en_rango(ficha: tuple[int, int]) -> bool:
    i, j = ficha
    if i < 0 or i > 7 or j < 0 or j > 7:
        return False
    else:
        return True


def evalua(s: np.ndarray) -> float:
    fichas = s.flat
    sum_negras = 0
    sum_blancas = 0
    total_fichas = 0
    for f in fichas:
        if f == Ficha.NEGRA:
            total_fichas += 1
            sum_negras += 1
        elif f == Ficha.BLANCA:
            total_fichas += 1
            sum_blancas += 1
    if total_fichas == 64:
        if sum_negras > sum_blancas:
            return 1
        elif sum_negras < sum_blancas:
            return -1
        else:
            return 0
    else:
        return (sum_negras - sum_blancas) / total_fichas


def cambiar_coordenadas(coord: tuple[int, int]) -> tuple[int, int]:
    x, y = coord
    nueva_x = 4 - x if x <= 3 else 3 - x
    nueva_y = y - 4 if y <= 3 else y - 3
    return (nueva_x, nueva_y)


def dist_manhattan(coord: tuple[int, int]) -> int:
    return abs(coord[0]) + abs(coord[1])


def ordena_jugadas(
    jugadas: list[tuple[int, int]], jugador: int
) -> list[tuple[int, int]]:
    def valor_jugada(jugada: tuple[int, int]) -> int:
        x, y = jugada
        coord = cambiar_coordenadas(jugada)
        d = dist_manhattan(coord)
        match d:
            case 2:
                return 4
            case 3:
                return 4
            case 4:
                if abs(x) == abs(y):
                    return 4
                else:
                    return 3
            case 5:
                return 3
            case 6:
                if abs(x) == abs(y):
                    return 1
                else:
                    return 4
            case 7:
                return 2
            case 8:
                return 5
            case _:
                return 1

    jugadas = sorted(jugadas, key=valor_jugada, reverse=True)
    return jugadas


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


def pretty_print_othello_con_jugadas_legales(s, juego: Othello, jugador: int):
    s_nuevo = s.copy()
    jugadas_legales = juego.jugadas_legales(s, jugador)
    for jugada in jugadas_legales:
        i, j = jugada
        s_nuevo[i][j] = 2
    print("\n   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
    separador_filas = "+---" * 8
    separador_filas = "---" + separador_filas + "+"
    print(separador_filas)
    for i in range(8):
        fila = s_nuevo[i]
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


def jugador_manual_othello(
    juego: Othello, s: np.ndarray, j: int
) -> tuple[int, int] | None:
    pretty_print_othello_con_jugadas_legales(s, juego, j)
    print(f"Turno de jugador {Ficha(j).name}")
    jugadas = juego.jugadas_legales(s, j)
    # print("Jugadas legales: ", jugadas)
    jugada = None
    while jugada not in jugadas:
        fila = int(input("Fila: "))
        columna = int(input("Columna: "))
        jugada = (fila, columna)
    return jugada


def juega_dos_jugadores_especial(juego, jugador1, jugador2):
    s, j = juego.inicializa()
    while not juego.terminal(s):
        a = jugador1(juego, s, j) if j == 1 else jugador2(juego, s, j)
        s = juego.transicion(s, a, j)
        j = -j
        char_jugador = "X" if -j == 1 else "O"
        print(f"Jugador {char_jugador} hizo {a} y el tablero quedo asi:")
        pretty_print_othello(s)
    return juego.ganancia(s), s


if __name__ == "__main__":
    modelo = Othello()
    print("=" * 40 + "\n" + "EL JUEGO DE OTHELLO".center(40) + "\n" + "=" * 40)

    jugs = []
    for j in [1, -1]:
        print(f"Selección de jugadores para las {' XO'[j]}:")
        sel = 0
        print("   1. Jugador manual")
        print("   2. Jugador negamax limitado en profundidad")
        print("   3. Jugador negamax limitado en tiempo")
        while sel not in [1, 2, 3]:
            sel = int(input(f"Jugador para las {' XO'[j]}: "))

        if sel == 1:
            jugs.append(jugador_manual_othello)
        elif sel == 2:
            d = None
            while type(d) is not int or d < 1:
                d = int(input("Profundidad: "))
            jugs.append(
                lambda juego, s, j: jugador_negamax(
                    juego, s, j, ordena=ordena_jugadas, evalua=evalua, d=d
                )
            )
        else:
            t = None
            while type(t) is not int or t < 1:
                t = int(input("Tiempo: "))
            tn = int(t)
            jugs.append(
                lambda juego, s, j: minimax_iterativo(
                    juego, s, j, ordena=ordena_jugadas, evalua=evalua, tiempo=tn
                )
            )

    g, s_final = juega_dos_jugadores_especial(modelo, jugs[0], jugs[1])
    print("\nSE ACABO EL JUEGO\n")
    pretty_print_othello(s_final)
    if g != 0:
        print("Gana el jugador " + " XO"[g])
    else:
        print("Empate")
