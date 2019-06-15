
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

    def adelante_D(self):
        return (self.vacio >> 4) & self.adelante[self.activo]
    def adelante_I(self):
        return (self.vacio >> 5) & self.adelante[self.activo]
    def atras_D(self):
        return (self.vacio << 4) & self.atras[self.activo]
    def atras_I(self):
        return (self.vacio << 5) & self.atras[self.activo]

    def sacar_movi(self):
        # Primero ve si hay un salto que se necesita hacer
        if self.salto:
            return self.saltos_obligatorios

        # movimiento normal
        else:
            AdD = self.adelante_D()
            AdI = self.adelante_I()
            AtD = self.atras_D()
            AtI = self.atras_I()

            moves =  [0x11 << i for (i, bit) in enumerate(bin(AdD)[::-1]) if bit == '1']
            moves += [0x21 << i for (i, bit) in enumerate(bin(AdI)[::-1]) if bit == '1']
            moves += [0x11 << i - 4 for (i, bit) in enumerate(bin(AtD)[::-1]) if bit == '1']
            moves += [0x21 << i - 5 for (i, bit) in enumerate(bin(AtI)[::-1]) if bit == '1']
            return moves


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