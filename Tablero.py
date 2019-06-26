
NEGRO, BLANCO  = 0, 1

BITS_no_usados = 0b100000000100000000100000000100000000

class Tablero:
    def __init__(self):
        self.adelante = [None, None]
        self.atras = [None, None]
        self.fichas = [None, None]
        self.juego_nuevo()

    def juego_nuevo(self):
        self.activo = NEGRO
        self.pasivo = BLANCO

        self.adelante[NEGRO] = 0x1eff
        self.atras[NEGRO] = 0
        self.fichas[NEGRO] = self.adelante[NEGRO] | self.atras[NEGRO]

        self.adelante[BLANCO] = 0
        self.atras[BLANCO] = 0x7fbc00000
        self.fichas[BLANCO] = self.adelante[BLANCO] | self.atras[BLANCO]

        self.vacio = BITS_no_usados ^ (2**36 - 1) ^ (self.fichas[NEGRO] | self.fichas[BLANCO])

        self.salto = 0
        self.saltos_obligatorios = []
    
    def hacer_movi(self, opcion):
        activo = self.activo
        pasivo = self.pasivo
        if opcion < 0:
            opcion *= -1
            taken_piece = int(1 << int ( sum(i for (i, b) in enumerate(bin(opcion)[::-1]) if b == '1')/2))
            self.fichas[pasivo] ^= taken_piece
            if self.adelante[pasivo] & taken_piece:
                self.adelante[pasivo] ^= taken_piece
            if self.atras[pasivo] & taken_piece:
                self.atras[pasivo] ^= taken_piece
            self.salto = 1

        self.fichas[activo] ^= opcion
        if self.adelante[activo] & opcion:
            self.adelante[activo] ^= opcion
        if self.atras[activo] & opcion:
            self.atras[activo] ^= opcion

        llegada = opcion & self.fichas[activo]
        self.vacio = BITS_no_usados ^ (2**36 - 1) ^ (self.fichas[NEGRO] | self.fichas[BLANCO]) 


        if activo == NEGRO and (llegada & 0x780000000) != 0:
            self.atras[NEGRO] |= llegada
        elif activo == BLANCO and (llegada & 0xf) != 0:
            self.adelante[BLANCO] |= llegada

        self.salto = 0
        self.activo, self.pasivo = self.pasivo, self.activo

    def ver_movimientos(self, opcion):
        B = self.copiar()
        activo = B.activo
        pasivo = B.pasivo
        if opcion < 0:
            opcion *= -1
            taken_piece = int(1 << sum(i for (i, b) in enumerate(bin(opcion)[::-1]) if b == '1')/2)
            B.fichas[pasivo] ^= taken_piece
            if B.adelante[pasivo] & taken_piece:
                B.adelante[pasivo] ^= taken_piece
            if B.atras[pasivo] & taken_piece:
                B.atras[pasivo] ^= taken_piece
            B.salto = 1

        B.fichas[activo] ^= opcion
        if B.adelante[activo] & opcion:
            B.adelante[activo] ^= opcion
        if B.atras[activo] & opcion:
            B.atras[activo] ^= opcion

        llegada = opcion & B.fichas[activo]
        B.vacio = BITS_no_usados ^ (2**36 - 1) ^ (B.fichas[NEGRO] | B.fichas[BLANCO])

        if B.salto:
            B.saltos_obligatorios = B.saltos_desde(llegada)
            if B.saltos_obligatorios: 
                return B

        if activo == NEGRO and (llegada & 0x780000000) != 0:
            B.atras[NEGRO] |= llegada
        elif activo == BLANCO and (llegada & 0xf) != 0:
            B.adelante[BLANCO] |= llegada

        B.salto = 0
        B.activo, B.pasivo = B.pasivo, B.activo

        return B

    def adelante_D(self):
        return (self.vacio >> 4) & self.adelante[self.activo]
    def adelante_I(self):
        return (self.vacio >> 5) & self.adelante[self.activo]
    def atras_D(self):
        return (self.vacio << 4) & self.atras[self.activo]
    def atras_I(self):
        return (self.vacio << 5) & self.atras[self.activo]
    def salto_adelante_D(self):
        return (self.vacio >> 8) & (self.fichas[self.pasivo] >> 4) & self.adelante[self.activo]
    def salto_adelante_I(self):
        return (self.vacio >> 10) & (self.fichas[self.pasivo] >> 5) & self.adelante[self.activo]
    def salto_atras_D(self):
        return (self.vacio << 8) & (self.fichas[self.pasivo] << 4) & self.atras[self.activo]
    def salto_atras_I(self):
        return (self.vacio << 10) & (self.fichas[self.pasivo] << 5) & self.atras[self.activo]

    def sacar_movi(self):
        # Primero ve si hay un salto que se necesita hacer
        if self.salto:
            return self.saltos_obligatorios

        # ver si hay muchos saltos this is missing in main code
        saltos = self.buscar_saltos()
        if saltos:
            return saltos

        # movimiento normal
        else:
            AdD = self.adelante_D()
            AdI = self.adelante_I()
            AtD = self.atras_D()
            AtI = self.atras_I()

            opciones =  [0x11 << i for (i, bit) in enumerate(bin(AdD)[::-1]) if bit == '1']
            opciones += [0x21 << i for (i, bit) in enumerate(bin(AdI)[::-1]) if bit == '1']
            opciones += [0x11 << i - 4 for (i, bit) in enumerate(bin(AtD)[::-1]) if bit == '1']
            opciones += [0x21 << i - 5 for (i, bit) in enumerate(bin(AtI)[::-1]) if bit == '1']
            return opciones
    
    def buscar_saltos(self):
        SAdD = self.salto_adelante_D()
        SAdI = self.salto_adelante_I()
        SAtD = self.salto_atras_D()
        SAtI = self.salto_atras_I()

        opciones = []

        if (SAdD | SAdI | SAtD | SAtI) != 0:
            opciones += [-0x101 << i for (i, bit) in enumerate(bin(SAdD)[::-1]) if bit == '1']
            opciones += [-0x401 << i for (i, bit) in enumerate(bin(SAdI)[::-1]) if bit == '1']
            opciones += [-0x101 << i - 8 for (i, bit) in enumerate(bin(SAtD)[::-1]) if bit == '1']
            opciones += [-0x401 << i - 10 for (i, bit) in enumerate(bin(SAtI)[::-1]) if bit == '1']

        return opciones
    
    def saltos_desde(self, piece):
        if self.activo == NEGRO:
            SAdD = (self.vacio >> 8) & (self.fichas[self.pasivo] >> 4) & piece
            SAdI = (self.vacio >> 10) & (self.fichas[self.pasivo] >> 5) & piece
            if piece & self.atras[self.activo]:
                SAtD = (self.vacio << 8) & (self.fichas[self.pasivo] << 4) & piece
                SAtI = (self.vacio << 10) & (self.fichas[self.pasivo] << 5) & piece
            else:
                SAtD = 0
                SAtI = 0
        else:
            SAtD = (self.vacio << 8) & (self.fichas[self.pasivo] << 4) & piece
            SAtI = (self.vacio << 10) & (self.fichas[self.pasivo] << 5) & piece
            if piece & self.adelante[self.activo]:
                SAdD = (self.vacio >> 8) & (self.fichas[self.pasivo] >> 4) & piece
                SAdI = (self.vacio >> 10) & (self.fichas[self.pasivo] >> 5) & piece
            else:
                SAdD = 0
                SAdI = 0

        opciones = []
        if (SAdD | SAdI | SAtD | SAtI) != 0:
            opciones += [-0x101 << i for (i, bit) in enumerate(bin(SAdD)[::-1]) if bit == '1']
            opciones += [-0x401 << i for (i, bit) in enumerate(bin(SAdI)[::-1]) if bit == '1']
            opciones += [-0x101 << i - 8 for (i, bit) in enumerate(bin(SAtD)[::-1]) if bit == '1']
            opciones += [-0x401 << i - 10 for (i, bit) in enumerate(bin(SAtI)[::-1]) if bit == '1']

        return opciones

    def tomable(self, piece):
        activo = self.activo
        if (self.adelante[activo] & (piece >> 4)) != 0 and (self.vacio & (piece << 4)) != 0:
            return True
        if (self.adelante[activo] & (piece >> 5)) != 0 and (self.vacio & (piece << 5)) != 0:
            return True
        if (self.atras[activo] & (piece << 4)) != 0 and (self.vacio & (piece >> 4)) != 0:
            return True
        if (self.atras[activo] & (piece << 5)) != 0 and (self.vacio & (piece >> 5)) != 0:
            return True
        return False

    def se_termino(self):
        return len(self.sacar_movi()) == 0

    def copiar(self):
        #Returna un tablero nuevo
        B = Tablero()
        B.activo = self.activo
        B.atras = [x for x in self.atras]
        B.vacio = self.vacio
        B.adelante = [x for x in self.adelante]
        B.salto = self.salto
        B.saltos_obligatorios = [x for x in self.saltos_obligatorios]
        B.pasivo = self.pasivo
        B.fichas = [x for x in self.fichas]
        return B

    def __str__(self):
        vacio = -1
        REY_NEGRO = 2
        REY_BLANCO = 3

        if self.activo == NEGRO:
            reyes_negros = self.atras[self.activo]
            peones_negros = self.adelante[self.activo] ^ reyes_negros
            reyes_blancos = self.adelante[self.pasivo]
            peones_blancos = self.atras[self.pasivo] ^ reyes_blancos
        else:
            reyes_negros = self.atras[self.pasivo]
            peones_negros = self.adelante[self.pasivo] ^ reyes_negros
            reyes_blancos = self.adelante[self.activo]
            peones_blancos = self.atras[self.activo] ^ reyes_blancos

        state = [[None for _ in range(8)] for _ in range(4)]
        for i in range(4):
            for j in range(8):
                cell = 1 << (9*i + j)
                if cell & peones_negros:
                    state[i][j] = NEGRO
                elif cell & peones_blancos:
                    state[i][j] = BLANCO
                elif cell & reyes_negros:
                    state[i][j] = REY_NEGRO
                elif cell & reyes_blancos:
                    state[i][j] = REY_BLANCO
                else:
                    state[i][j] = vacio

        Tablero = [None] * 17
        for i in range(9):
            Tablero[2*i] = ["  ├"] + ["───┼"]*7 + ["───┤", "\n"]
            if i==0:
                 Tablero[2*i] = ["  ╭"] + ["───┬"]*7 + ["───╮", "\n"]
            if i < 8:
                Tablero[2*i + 1] = ["  |", "   "] \
                             + [a for subl in [["|", "   "] for _ in range(7)] for a in subl] \
                             + ["|", "\n"]
            if i==8:
                Tablero[2*i] = ["  ╰"] + ["───┴"]*7 + ["───╯", "\n"]
            
        for i, chunk in enumerate(state):
            for j, cell in enumerate(chunk):
                if j < 4:
                    if cell == NEGRO:
                        Tablero[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "n" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == BLANCO:
                        Tablero[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "b" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == REY_NEGRO:
                        Tablero[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "N" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == REY_BLANCO:
                        Tablero[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                "B" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    else:
                        Tablero[2*(7 - 2*i) + 1][2*(6 - 2*j) + 1] = \
                                " " + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                else:
                    if cell == NEGRO:
                        Tablero[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "n" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == BLANCO:
                        Tablero[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "b" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == REY_NEGRO:
                        Tablero[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "N" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    elif cell == REY_BLANCO:
                        Tablero[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                "B" + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')
                    else:
                        Tablero[2*(6 - 2*i) + 1][2*(7 - 2*j) - 1] = \
                                " " + str(1 + j + 8*i) + (' ' if j + 8*i < 9 else '')

        return "".join(map(lambda x: "".join(x), Tablero))