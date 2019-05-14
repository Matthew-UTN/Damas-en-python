from Tablero import *
from IA import minMax2


ancho = 0
tmp = 0
largo = 0
primerjugador = 0

# movimiento del usario
def sacarMoviJugador(b):
    string1 = "Selecciona una de tus fichas eg. " + chr(b.listaBlanco[0][0]+97) + str(b.listaBlanco[0][1])
    print(string1)
    while True: 
        movimiento = []
        movimiento = input().lower().split()
        if not(len(movimiento) == 2):
            print ("Eso no es un movimiento valido.", string1)
            continue
        moviDesde = (int(movimiento[0][1]), ord(movimiento[0][0]) - 97)
        moviHasta = (int(movimiento[1][1]), ord(movimiento[1][0]) - 97)
        if not (moviDesde in b.listaBlanco):
            print ("La ficha ", moviDesde, "no es tuya.")
            continue
        break
    movimiento = (moviDesde, moviHasta, b.NOTERMINADO)
    return movimiento

# Main 
print("Bienvenido")
while True:
  tmp=int(input("Selecciona el tamaño del tablero entre 6 y 10."))
  if (tmp>5):
    if(tmp<11):
      break

ancho = tmp
largo = tmp
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
