from copy import deepcopy


def ha_ganado(Tablero):
    """
        Devuelve True si el juego fue ganado.
    """
    return Tablero.juegoGanado != Tablero.NOTERMINADO


def minMax2(Tablero):
    """
        Toma un tablero como entrada y devuelve el mejor movimiento en forma de tablero.
    """
    mejorTablero = None
    currentDepth = Tablero.maxDepth + 1
    while not mejorTablero and currentDepth > 0:
        currentDepth -= 1
        # Trae el mejor movimiento y su valor desde maxMinTablero.
        (mejorTablero, mejorValor) = maxMove2(Tablero, currentDepth)

        # Si trae un tablero null lanzamos una excepción.
    if not mejorTablero:
        raise Exception("Solo puede devolver tableros no nulos.")
    else:
        return (mejorTablero, mejorValor)


def maxMove2(maxTablero, currentDepth):
    """
        Calcula el mejor movimiento para el jugador Negro(busca conseguir que el Tablero este en inf)
    """
    return maxMinTablero(maxTablero, currentDepth - 1, float('-inf'))


def minMove2(minTablero, currentDepth):
    """
        Calcula el mejor movimiento para el jugador Blanco(busca conseguir que el Tablero este en -inf)
    """
    return maxMinTablero(minTablero, currentDepth - 1, float('inf'))


def maxMinTablero(Tablero, currentDepth, mejorMovimiento):
    """
        Aca se calcula realmente el movimiento
    """
    # Chequea si estamos en un nodo final
    if ha_ganado(Tablero) or currentDepth <= 0:
        return (Tablero, staticEval2(Tablero))

    # Si no estamos en el nodo final hacemos mixMan
    # Seteamos valores para minmax
    mejor_mov = mejorMovimiento
    mejor_tablero = None

    # NodoMaximo
    if mejorMovimiento == float('-inf'):
        # Creamos la iteracion de los movimientos
        movimientos = Tablero.iterNegroMueve()
        for movimiento in movimientos:
            maxTablero = deepcopy(Tablero)
            maxTablero.movimientoSilentNegro(*movimiento)
            valor = minMove2(maxTablero, currentDepth - 1)[1]
            if valor > mejor_mov:
                mejor_mov = valor
                mejor_tablero = maxTablero

    # NodoMinimo
    elif mejorMovimiento == float('inf'):
        movimientos = Tablero.iterBlancoMueve()
        for movimiento in movimientos:
            minTablero = deepcopy(Tablero)
            minTablero.movimientoSilentBlanco(*movimiento)
            valor = maxMove2(minTablero, currentDepth - 1)[1]
            # Tomamos el valor mas bajo que podamos
            if valor < mejor_mov:
                mejor_mov = valor
                mejor_tablero = minTablero

    # Si hay algo erroneo con mejorMovimiento largamos una excepcion
    else:
        raise Exception("mejorMovimiento no puede ser otra cosa que no sea -inf o inf")

    # Devuelve el mejor movimiento
    return (mejor_tablero, mejor_mov)


def staticEval2(evalTablero):
    """
        Evalua un tablero que tan ventajoso es
        -INF si el jugador Blanco ha ganado
        INF si el jugador Negro ha ganado
        De otra forma usa una estrategia particular para evaluar el movimiento
    """
    # ¿Alguien a ganado el juego? Si es asi devuelve un valor INF
    if evalTablero.juegoGanado == evalTablero.NEGRO:
        return float('inf')
    elif evalTablero.juegoGanado == evalTablero.BLANCO:
        return float('-inf')


    # Iniciar variables
    score = 0
    pieces = None
    if evalTablero.turno == evalTablero.BLANCO:
        pieces = evalTablero.listaBlanco
        scoremod = -1
    elif evalTablero.turno == evalTablero.NEGRO:
        pieces = evalTablero.listaNegro
        scoremod = 1

    # Super Gigadeath Defensa Evaluador
    # Esta AI va a intentar mantener todas las piezas lo mas cercana posible hasta que tenga la chance de saltar
    # al jugador oponente. Es super efectivo
    distance = 0
    for piece1 in pieces:
        for piece2 in pieces:
            if piece1 == piece2:
                continue
            dx = abs(piece1[0] - piece2[0])
            dy = abs(piece1[1] - piece2[1])
            distance += dx ** 2 + dy ** 2
    distance /= len(pieces)
    score = 1.0 / distance * scoremod

    return score
