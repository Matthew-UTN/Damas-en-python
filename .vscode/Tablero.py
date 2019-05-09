class Tablero(object):
    NEGRO = 1
    BLANCO = 0
    NOTERMINADO = -1
    def __init__(self, largo, ancho, primerJugador):
        """
            Hace un Tablero, maxDepth esta assignado manualmente
        """
        # hace el largo y ancho del tablero
        self.ancho = ancho
        self.largo = largo
        # hace dos listas adonde se guarda que piesas tiene cada jugador
        self.listaNegro = []
        self.listaBlanco = []
        # posiciones de inicio
        for i in range(ancho):
            self.listaNegro.append((i, (i+1)%2))
            self.listaBlanco.append((i, largo - (i%2) - 1))
        # TableroState contiene el estado actual del Tablero para mostrar
        self.TableroState = [[' '] * self.ancho for x in range(self.largo)]
        self.juegoGanado = self.NOTERMINADO
        self.turno = primerJugador
        self.maxDepth = 10

    def printTablero(self):

        print (unicode(self))
        
    def __unicode__(self):
        
        # actualiza el Tablero
        self.actualizarTablero()
        lineas = []
        # muestra los numeros arriba del tablero
        lineas.append('    ' + '   '.join(map(str, range(self.ancho))))
        # imprimo el tablero
        lineas.append(u'  ╭' + (u'───┬' * (self.ancho-1)) + u'───╮')

        for num, row in enumerate(self.TableroState[:-1]):
            lineas.append(chr(num+65) + u' │ ' + u' │ '.join(row) + u' │')
            lineas.append(u'  ├' + (u'───┼' * (self.ancho-1)) + u'───┤')
        
        lineas.append(chr(self.largo+64) + u' │ ' + u' │ '.join(self.TableroState[-1]) + u' │')

        lineas.append(u'  ╰' + (u'───┴' * (self.ancho-1)) + u'───╯')
        return '\n'.join(lineas)


    