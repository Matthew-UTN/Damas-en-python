class IA_Damas:
    def __init__(self, funcion_de_movimiento):
        self.funcion_de_movimiento = funcion_de_movimiento

    def hacer_movi(self, Tablero):
        return self.funcion_de_movimiento(Tablero)