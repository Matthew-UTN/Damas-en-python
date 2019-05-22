class Tablero(object):
    NEGRO = 1
    BLANCO = 0
    NOTERMINADO = -1
    def __init__(self, largo, ancho, primerJugador):
        
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
        for i in range(4):
            self.listaNegro.append((1+(i*2), 2))
            self.listaBlanco.append((0+(i*2), 5))
        # TableroState contiene el estado actual del Tablero para mostrar
        self.TableroState = [[' '] * self.ancho for x in range(self.largo)]
        self.juegoGanado = self.NOTERMINADO
        self.turno = primerJugador
        self.maxDepth = 10

    # genera movimientos
    def iterBlancoMueve(self):
        """
            Generador de movimientos del blanco
        """
        for ficha in self.listaBlanco:
            for movimiento in self.iterBlancoFicha(ficha):
                yield movimiento
                
    def iterNegroMueve(self):
        """
            Generador de movimientos del negro
        """
        for ficha in self.listaNegro:
            for movimiento in self.iterNegroFicha(ficha):
                yield movimiento
                
    def iterBlancoFicha(self, ficha):
        """
            genera movimientos posibles para la ficha blanca
        """            
        return self.iterBoth(ficha, ((-1,-1),(1,-1)))
    
    def iterNegroFicha(self, ficha):
        """
            genera movimientos posibles para la ficha negra
        """
        return self.iterBoth(ficha, ((-1,1),(1,1)))

    def iterBoth(self, ficha, movimientos):
        """
            Maneja la generación real de movimientos para fichas negras o blancas.
        """
        for movimiento in movimientos:
            # Movimiento regular
            targetx = ficha[0] + movimiento[0]
            targety = ficha[1] + movimiento[1]
            # si el movimiento esta fuera del area no mueve
            if targetx < 0 or targetx >= self.ancho or targety < 0 or targety >= self.largo:
                continue
            target = (targetx, targety)
            # Compruebe que no haya nada que impide movimiento.
            negro = target in self.listaNegro
            blanco = target in self.listaBlanco
            if not negro and not blanco:
                yield (ficha, target, self.NOTERMINADO)
            # verifica si puede saltar
            else:
                # tiene que ser del color opuesto
                if self.turno == self.NEGRO and negro:
                    continue
                elif self.turno == self.BLANCO and blanco:
                    continue
                # Salta procediendo agregando el mismo movimiento para saltar sobre el oponente 
                # ficha en el tablero
                jumpx = target[0] + movimiento[0]
                jumpy = target[1] + movimiento[1]
                # verifica que no salga del area si salta
                if jumpx < 0 or jumpx >= self.ancho or jumpy < 0 or jumpy >= self.largo:
                    continue
                jump = (jumpx, jumpy)
                # verifica que no haya nada en la posicion que va saltar
                negro = jump in self.listaNegro
                blanco = jump in self.listaBlanco
                if not negro and not blanco:
                    yield (ficha, jump, self.turno) 

    def actualizarTablero(self):
        """
            Actualiza la array que contiene el Tablero para reflejar el estado actual de las fichas en el
            tablero
        """
        for i in range(self.ancho):
            for j in range(self.largo):
                self.TableroState[i][j] = " "
        for ficha in self.listaNegro:
            self.TableroState[ficha[1]][ficha[0]] = u'◆'
        for ficha in self.listaBlanco:
            self.TableroState[ficha[1]][ficha[0]] = u'◇'
    
    # movimiento de fichas
    def movimientoSilentNegro(self, movimientoDesde, movimientoAdondeSeVa, Resultado): 
        """
            Movimiento de la ficha negra sin print
        """
        if movimientoAdondeSeVa[0] < 0 or movimientoAdondeSeVa[0] >= self.ancho or movimientoAdondeSeVa[1] < 0 or movimientoAdondeSeVa[1] >= self.largo:
            raise Exception("Eso moveria la ficha negra", movimientoDesde, "fuera del area")
        negro = movimientoAdondeSeVa in self.listaNegro
        blanco = movimientoAdondeSeVa in self.listaBlanco
        if not (negro or blanco):
            self.listaNegro[self.listaNegro.index(movimientoDesde)] = movimientoAdondeSeVa
            self.actualizarTablero()
            self.turno = self.BLANCO
            #self.juegoGanado = Resultado
        else:
            raise Exception
        
    def movimientoSilentBlanco(self, movimientoDesde, movimientoAdondeSeVa, Resultado):
        """
            Movimiento de la ficha blanca sin print
        """
        if movimientoAdondeSeVa[0] < 0 or movimientoAdondeSeVa[0] >= self.ancho or movimientoAdondeSeVa[1] < 0 or movimientoAdondeSeVa[1] >= self.largo:
            raise Exception("Eso moveria la ficha blanca", movimientoDesde, "fuera del area")
        negro = movimientoAdondeSeVa in self.listaNegro
        blanco = movimientoAdondeSeVa in self.listaBlanco
        if not (negro or blanco):
            self.listaBlanco[self.listaBlanco.index(movimientoDesde)] = movimientoAdondeSeVa
            self.actualizarTablero()
            self.turno = self.NEGRO
            #self.juegoGanado = Resultado
        else:
            raise Exception
    
    def movimientoNegro(self, movimientoDesde, movimientoAdondeSeVa, Resultado):
        """
            Movimiento a negro ficha de un lugar a otro. Resultado se pasa como 0 (blanco)
            o 1 (negro) si el movimiento es un salto.
        """
        self.movimientoSilentNegro(movimientoDesde, movimientoAdondeSeVa, Resultado)
        self.printTablero()
        
    def movimientoBlanco(self, movimientoDesde, movimientoAdondeSeVa, Resultado):
        """
            Movimiento a blanco ficha de un lugar a otro. Resultado se pasa como 0 (blanco)
            o 1 (negro) si el movimiento es un salto.
        """
        self.movimientoSilentBlanco(movimientoDesde, movimientoAdondeSeVa, Resultado)
        self.printTablero()

    def printTablero(self):

        print (str(self))
        
    def __str__(self):
        
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