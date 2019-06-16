import Tablero
import sys

NEGRO, BLANCO = 0, 1

def main():
    print ("Bienvenido")

    n = -1
    while not n in [1, 2]:
        n = input("Cantidad de jugadores humanos? (1, 2): ")
        try:
            n = int(n)
        except ValueError:
            print ("Ingrese 1, or 2.")

    if n == 2:
        B = Tablero.Tablero()
        print ("Negro va primero.")
        Turno = 1
        while not termino(B):
            print(B)
            Movimientos = B.sacar_movi()
            for (i, move) in enumerate(strings_movi(B)):
                print ("Opcion " + str(i) + ": " + move)
            while True:
                movi_idx = input("Ingrese que movimiento quieres hacer: ")
                try:
                    movi_idx = int(movi_idx)
                except ValueError:
                    print ("Ingrese un numero valido.")
                    continue
                if movi_idx in range(len(Movimientos)):
                    break
                else:
                    print ("Ingrese un numero valido.")
                    continue
            B.hacer_movi(Movimientos[movi_idx])
            Turno += 1

        print (B)


def termino(Tablero):
    return len(Tablero.sacar_movi()) == 0

def strings_movi(Tablero):
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

if __name__ == '__main__':
    main()
