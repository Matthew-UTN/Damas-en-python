from Tablero import *
from IA import minMax2


ancho = 8
largo = 8
primerjugador = 0

# movimiento del usario
def sacarMoviJugador(b):
    string1 = "Hagas un movimiento (eg. " + chr(b.listaBlanco[0][0]+102) + str(b.listaBlanco[0][0]) + " " + chr(b.listaBlanco[0][0]+101) + str(b.listaBlanco[1][0])+")"
    print(string1)
    while True: 
        movimiento = []
        movimiento = input().lower().split()
        if not(len(movimiento) == 2):
            print ("Eso no es un movimiento valido.", string1)
            continue
        if (int(movimiento[0][1]) == int(movimiento[1][1])-1 | int(movimiento[0][1]) == int(movimiento[1][1])-1):
            moviDesde = (int(movimiento[0][1]), ord(movimiento[0][0]) - 97)
            moviHasta = (int(movimiento[1][1]), ord(movimiento[1][0]) - 97)
        else:
            print ("Eso no es diagonal", string1)
            continue
        if not (moviDesde in b.listaBlanco):
            print ("La ficha ", moviDesde, "no es tuya.")
            continue
        break
    movimiento = (moviDesde, moviHasta, b.NOTERMINADO)
    return movimiento

# Main 
print("Bienvenido")
b = Tablero(ancho, largo, primerjugador)
b.printTablero()


while b.juegoGanado == -1:
    moviJugador = sacarMoviJugador(b)
    try:
        b.movimientoBlanco(*moviJugador)
    except Exception:
        print ("Movimiento invalido")
        continue
        
    temp = minMax2(b)
    b = temp[0]
    print ("**********I.A**********")
    b.printTablero()
    if b.juegoGanado == b.BLANCO:
        print ("Blanco gana\nPartida terminada")
        break
    elif b.juegoGanado == b.NEGRO:
        print ("Negro gana\nPartida terminada")
        break
