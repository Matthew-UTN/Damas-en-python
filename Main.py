from Tablero import *

ancho = 0
tmp = 0
largo = 0
primerjugador = 0

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