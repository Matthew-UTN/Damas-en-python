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


def negar(Tablero):  #Negacion de ocupaciones

    AdD = Tablero.adelante_D()
    AdI = Tablero.adelante_I()
    AtD = Tablero.atras_D()
    AtI = Tablero.atras_I()

    opciones = [0x11 << i for (i, bit) in enumerate(bin(AdD)[::-1]) if bit == '1']
    opciones += [0x21 << i for (i, bit) in enumerate(bin(AdI)[::-1]) if bit == '1']
    opciones += [0x11 << i - 4 for (i, bit) in enumerate(bin(AtD)[::-1]) if bit == '1']
    opciones += [0x21 << i - 5 for (i, bit) in enumerate(bin(AtI)[::-1]) if bit == '1']

    llegadas = [0x10 << i for (i, bit) in enumerate(bin(AdD)[::-1]) if bit == '1']
    llegadas += [0x20 << i for (i, bit) in enumerate(bin(AdI)[::-1]) if bit == '1']
    llegadas += [0x1 << i - 4 for (i, bit) in enumerate(bin(AtD)[::-1]) if bit == '1']
    llegadas += [0x1 << i - 5 for (i, bit) in enumerate(bin(AtI)[::-1]) if bit == '1']

    negaciones = []

    for opcion, dest in zip(opciones, llegadas):
        B = Tablero.ver_movimientos(opcion)
        activo = B.activo
        ms_tomar = []
        ds = []
        if (B.adelante[activo] & (dest >> 4)) != 0 and (B.vacio & (dest << 4)) != 0:
            ms_tomar.append((-1) * ((dest >> 4) | (dest << 4)))
            ds.append(dest << 4)
        if (B.adelante[activo] & (dest >> 5)) != 0 and (B.vacio & (dest << 5)) != 0:
            ms_tomar.append((-1) * ((dest >> 5) | (dest << 5)))
            ds.append(dest << 5)
        if (B.atras[activo] & (dest << 4)) != 0 and (B.vacio & (dest >> 4)) != 0:
            ms_tomar.append((-1) * ((dest << 4) | (dest >> 4)))
            ds.append(dest >> 4)
        if (B.atras[activo] & (dest << 5)) != 0 and (B.vacio & (dest >> 5)) != 0:
            ms_tomar.append((-1) * ((dest << 5) | (dest >> 5)))
            ds.append(dest >> 5)

        if not ms_tomar:
            continue
        else:
            for m, d in zip(ms_tomar, ds):
                C = B.ver_movimientos(m)
                if C.activo == activo:
                    if not dest in negaciones:
                        negaciones.append(dest)
                    continue
                if not C.takeable(d):
                    if not dest in negaciones:
                        negaciones.append(dest)

    return len(negaciones)


def kcent(Tablero):  # Control del centro con un rey

    pasivo = Tablero.pasivo
    if pasivo == BLANCO:
        fichas_del_centro = 0xA619800
        pasivo_kings = Tablero.adelante[BLANCO]
    else:
        fichas_del_centro = 0xCC3280
        pasivo_kings = Tablero.atras[NEGRO]

    return bin(pasivo_kings & fichas_del_centro).count("1")


def mob(Tablero):  # movimiento total

    AdD = Tablero.adelante_D()
    AdI = Tablero.adelante_I()
    AtD = Tablero.atras_D()
    AtI = Tablero.atras_I()

    llegadas = [0x10 << i for (i, bit) in enumerate(bin(AdD)[::-1]) if bit == '1']
    llegadas += [0x20 << i for (i, bit) in enumerate(bin(AdI)[::-1]) if bit == '1']
    llegadas += [0x1 << i - 4 for (i, bit) in enumerate(bin(AtD)[::-1]) if bit == '1']
    llegadas += [0x1 << i - 5 for (i, bit) in enumerate(bin(AtI)[::-1]) if bit == '1']

    if not llegadas:
        return 0
    return bin(reduce(lambda x, y: x | y, llegadas)).count("1")

def mobil(Tablero): # Movilidad posible

    return mob(Tablero) - negar(Tablero)

def mov(Tablero): # opciones que puede tomar el IA

    peones_negros = bin(Tablero.adelante[NEGRO]).count("1")
    reyes_negros = bin(Tablero.atras[NEGRO]).count("1")
    puntaje_negro = 2*peones_negros + 3*reyes_negros
    peones_blancos = bin(Tablero.atras[BLANCO]).count("1")
    reyes_blancos = bin(Tablero.adelante[BLANCO]).count("1")
    puntaje_blanco = 2*peones_blancos + 3*reyes_blancos

    if puntaje_blanco < 24 and puntaje_negro == puntaje_blanco:
        fichas = Tablero.fichas[NEGRO] | Tablero.fichas[BLANCO]
        if Tablero.activo == NEGRO:
            sistema_de_movimiento =  0x783c1e0f
        else:
            sistema_de_movimiento = 0x783c1e0f0
        if bin(sistema_de_movimiento & fichas).count("1") % 2 == 1:
            return 1

    return 0

def peligro(Tablero):

    opciones = Tablero.sacar_movi()
    llegadas = map(lambda x: (x ^ Tablero.fichas[Tablero.activo]) & x, opciones)
    origenes = [x ^ y for (x, y) in zip(opciones, llegadas)]

    saltos = []
    for dest, orig in zip(llegadas, origenes):
        if Tablero.activo == NEGRO:
            SAdD = (Tablero.vacio >> 8) & (Tablero.fichas[Tablero.pasivo] >> 4) & dest
            SAdI = (Tablero.vacio >> 10) & (Tablero.fichas[Tablero.pasivo] >> 5) & dest
            if orig & Tablero.atras[Tablero.activo]: # piece is king
                SAtD = (Tablero.vacio << 8) & (Tablero.fichas[Tablero.pasivo] << 4) & dest
                SAtI = (Tablero.vacio << 10) & (Tablero.fichas[Tablero.pasivo] << 5) & dest
            else:
                SAtD = 0
                SAtI = 0
        else:
            SAtD = (Tablero.vacio << 8) & (Tablero.fichas[Tablero.pasivo] << 4) & dest
            SAtI = (Tablero.vacio << 10) & (Tablero.fichas[Tablero.pasivo] << 5) & dest
            if dest & Tablero.adelante[Tablero.activo]: # piece at square is a king
                SAdD = (Tablero.vacio >> 8) & (Tablero.fichas[Tablero.pasivo] >> 4) & dest
                SAdI = (Tablero.vacio >> 10) & (Tablero.fichas[Tablero.pasivo] >> 5) & dest
            else:
                SAdD = 0
                SAdI = 0

        if (SAdD | SAdI | SAtD | SAtI) != 0:
            saltos += [-0x101 << i for (i, bit) in enumerate(bin(SAdD)[::-1]) if bit == '1']
            saltos += [-0x401 << i for (i, bit) in enumerate(bin(SAdI)[::-1]) if bit == '1']
            saltos += [-0x101 << i - 8 for (i, bit) in enumerate(bin(SAtD)[::-1]) if bit == '1']
            saltos += [-0x401 << i - 10 for (i, bit) in enumerate(bin(SAtI)[::-1]) if bit == '1']

    return len(saltos)

def diferencia_de_fichas(Tablero, player):
    peones_negros = bin(Tablero.adelante[NEGRO]).count("1")
    reyes_negros = bin(Tablero.atras[NEGRO]).count("1")
    puntaje_negro = 2*peones_negros + 3*reyes_negros
    peones_blancos = bin(Tablero.atras[BLANCO]).count("1")
    reyes_blancos = bin(Tablero.adelante[BLANCO]).count("1")
    puntaje_blanco = 2*peones_blancos + 3*reyes_blancos

    return puntaje_negro - puntaje_blanco if player == NEGRO else puntaje_blanco - puntaje_negro

def posiciones(Tablero, player):
    puntajes = [0x88000, 0x1904c00, 0x3A0502E0, 0x7C060301F]
    i = 1
    total = 0
    for s in puntajes:
        total = i*bin(Tablero.fichas[player] & s).count("1")
        i += 1
    return total

def puntaje(Tablero_viejo, Tablero_nuevo):
    if Tablero_viejo.se_termino():
        return -INFINITO
    if Tablero_nuevo.se_termino():
        return INFINITO
    _adv   = adv(Tablero_nuevo) - adv(Tablero_viejo)
    _atras  = adv(Tablero_nuevo) - atras(Tablero_viejo)
    _cent  = cent(Tablero_nuevo) - cent(Tablero_viejo)
    _cntr  = cntr(Tablero_nuevo) - cntr(Tablero_viejo)
    _negar  = negar(Tablero_nuevo) - negar(Tablero_viejo)
    _kcent = kcent(Tablero_nuevo) - kcent(Tablero_viejo)
    _mob   = mob(Tablero_nuevo) - mob(Tablero_viejo)
    _mobil = _mob - _negar
    _mov   = mov(Tablero_nuevo) - mov(Tablero_viejo)
    _peligro = peligro(Tablero_nuevo) - peligro(Tablero_viejo)

    mobilidad_que_no_esta_negado = 1 if _mobil > 0 else 0
    mobilidad_total = 1 if _mob > 0 else 0
    negacion_de_occ = 1 if _negar > 0 else 0
    control = 1 if _cent > 0 else 0

    _demmo = 1 if negacion_de_occ and not mobilidad_total else 0
    _modo_2 = 1 if mobilidad_que_no_esta_negado and not negacion_de_occ else 0
    _modo_3 = 1 if not mobilidad_que_no_esta_negado and negacion_de_occ else 0
    _moc_2 = 1 if not mobilidad_que_no_esta_negado and control else 0
    _moc_3 = 1 if mobilidad_que_no_esta_negado and not control else 0
    _moc_4 = 1 if not mobilidad_que_no_esta_negado and not control else 0

    Tablero_puntaje = _moc_2*(-1)*(2**18)  \
                + _kcent*(2**16)       \
                + _moc_4*(-1)*(2**14)  \
                + _modo_3*(-1)*(2**13) \
                + _demmo*(-1)*(2**11)  \
                + _mov*(2**8)          \
                + _adv*(-1)*(2**8)     \
                + _modo_2*(-1)*(2**8)  \
                + _atras*(-1)*(2**6)    \
                + _cntr*(2**5)         \
                + _peligro*(2**5)        \
                + _moc_3*(2**4)        \
                + diferencia_de_fichas(Tablero_nuevo, Tablero_viejo.activo)*(2**20) \
                + posiciones(Tablero_nuevo, Tablero_viejo.activo)*(2**14)

    return Tablero_puntaje

def negamax(Tablero_viejo, Tablero_nuevo, profundo, alpha, beta, color):
    if profundo == 0 or Tablero_nuevo.se_termino():
        return puntaje(Tablero_viejo, Tablero_nuevo)*color
    mejor_valor = -INFINITO
    for opcion in Tablero_nuevo.sacar_movi():
        B = Tablero_nuevo.ver_movimientos(opcion)
        if B.activo != Tablero_nuevo.activo:
            val = -negamax(Tablero_nuevo, B, profundo - 1, -beta, -alpha, -color)
        else:
            val = negamax(Tablero_nuevo, B, profundo, alpha, beta, color)
        mejor_valor = max(mejor_valor, val)
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return mejor_valor

def funcion_de_movimiento(Tablero, profundo=7):
    def buscar(opcion):
        B = Tablero.ver_movimientos(opcion)
        if B.activo == Tablero.activo:
            return negamax(Tablero, B, profundo, -INFINITO, INFINITO, 1)
        else:
            return negamax(Tablero, B, profundo, -INFINITO, INFINITO, -1)

    return max(Tablero.sacar_movi(), key=buscar)

def strings_movi(Tablero):
    SAdD = Tablero.salto_adelante_D()
    SAdI = Tablero.salto_adelante_I()
    SAtD = Tablero.salto_atras_D()
    SAtI = Tablero.salto_atras_I()

    if (SAdD | SAdI | SAtD | SAtI) != 0:
        SAdD = [(1 + i - i//9, 1 + (i + 8) - (i + 8)//9)
                    for (i, bit) in enumerate(bin(SAdD)[::-1]) if bit == '1']
        SAdI = [(1 + i - i//9, 1 + (i + 10) - (i + 8)//9)
                    for (i, bit) in enumerate(bin(SAdI)[::-1]) if bit == '1']
        SAtD = [(1 + i - i//9, 1 + (i - 8) - (i - 8)//9)
                    for (i, bit) in enumerate(bin(SAtD)[::-1]) if bit ==  '1']
        SAtI = [(1 + i - i//9, 1 + (i - 10) - (i - 10)//9)
                    for (i, bit) in enumerate(bin(SAtI)[::-1]) if bit == '1']

        if Tablero.activo == NEGRO:
            movi_reg = ["%i to %i" % (orig, dest) for (orig, dest) in SAdD + SAdI]
            movi_inversa = ["%i to %i" % (orig, dest) for (orig, dest) in SAtD + SAtI]
            return movi_reg + movi_inversa
        else:
            movi_inversa = ["%i to %i" % (orig, dest) for (orig, dest) in SAdD + SAdI]
            movi_reg = ["%i to %i" % (orig, dest) for (orig, dest) in SAtD + SAtI]
            return movi_inversa + movi_reg


    AdD = Tablero.adelante_D()
    AdI = Tablero.adelante_I()
    AtD = Tablero.atras_D()
    AtI = Tablero.atras_I()

    AdD = [(1 + i - i//9, 1 + (i + 4) - (i + 4)//9)
                for (i, bit) in enumerate(bin(AdD)[::-1]) if bit == '1']
    AdI = [(1 + i - i//9, 1 + (i + 5) - (i + 5)//9)
                for (i, bit) in enumerate(bin(AdI)[::-1]) if bit == '1']
    AtD = [(1 + i - i//9, 1 + (i - 4) - (i - 4)//9)
                for (i, bit) in enumerate(bin(AtD)[::-1]) if bit ==  '1']
    AtI = [(1 + i - i//9, 1 + (i - 5) - (i - 5)//9)
                for (i, bit) in enumerate(bin(AtI)[::-1]) if bit == '1']

    if Tablero.activo == NEGRO:
        movi_reg = ["%i to %i" % (orig, dest) for (orig, dest) in AdD + AdI]
        movi_inversa = ["%i to %i" % (orig, dest) for (orig, dest) in AtD + AtI]
        return movi_reg + movi_inversa
    else:
        movi_reg = ["%i to %i" % (orig, dest) for (orig, dest) in AtD + AtI]
        movi_inversa = ["%i to %i" % (orig, dest) for (orig, dest) in AdD + AdI]
        return movi_inversa + movi_reg