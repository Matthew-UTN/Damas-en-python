import sys

NEGRO, BLANCO = 0, 1
lugares_validos = 0x7FBFDFEFF

INFINITO = sys.maxsize

def adv(Tablero):
    pasivo = Tablero.pasivo

    filas_3_y_4 =   0x1FE00
    filas_5_y_6 = 0x3FC0000
    if pasivo == BLANCO:
        filas_3_y_4, filas_5_y_6 = filas_5_y_6, filas_3_y_4

    bits_3_and_4 = filas_3_y_4 & Tablero.fichas[pasivo]
    bits_5_and_6 = filas_5_y_6 & Tablero.fichas[pasivo]
    return bin(bits_5_and_6).count("1") - bin(bits_3_and_4).count("1")

def atras(Tablero):

    activo = Tablero.activo
    pasivo = Tablero.pasivo
    if activo == NEGRO:
        if Tablero.atras[NEGRO] != 0:
            return 0
        fila_de_atras = 0x480000000
    else:
        if Tablero.adelante[BLANCO] != 0:
            return 0
        fila_de_atras = 0x5

    if bin(fila_de_atras & Tablero.fichas[pasivo]).count('1') == 2:
        return 1
    return 0

def cent(Tablero):
    pasivo = Tablero.pasivo
    if pasivo == BLANCO:
        fichas_del_centro = 0xA619800
    else:
        fichas_del_centro = 0xCC3280

    return bin(Tablero.fichas[pasivo] & fichas_del_centro).count("1")

def cntr(Tablero):
    activo = Tablero.activo
    if activo == NEGRO:
        fichas_del_centro = 0xA619800
    else:
        fichas_del_centro = 0xCC3280

    cant_de_activos_centro = bin(Tablero.fichas[activo] & fichas_del_centro).count("1")

    opciones = Tablero.sacar_movi()
    if opciones[0] < 0:
        opciones = map(lambda x: x*(-1), opciones)
    llegadas = reduce(lambda x, y: x|y,
                          [(m & (m ^ Tablero.fichas[activo])) for m in opciones])

    cant_de_activos_cerca_de_centro = bin(llegadas & fichas_del_centro).count("1")

    return cant_de_activos_centro + cant_de_activos_cerca_de_centro