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
        jugador_actual = B.activo
        while not termino(B):
            print(B)

            Movimientos = B.sacar_movi()

            if B.salto:
                print ("Salto.")
                print ("")
            else:
                print ("Turno %i" % Turno)
                print ("")

            for (i, opcion) in enumerate(strings_movi(B)):
                print ("opcion " + str(i) + ": " + opcion)

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

            if B.activo == jugador_actual:
                print ("Debe saltar.")
                continue
            else:
                jugador_actual = B.activo
                Turno += 1

        print (B)
        if B.activo == BLANCO:
            print ("Gano negro!")
        else:
            print ("Gano blanco!")

        return 0


def termino(Tablero):
    return len(Tablero.sacar_movi()) == 0

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
            movi_reg = ["%i a %i" % (orig, dest) for (orig, dest) in SAdD + SAdI]
            movi_inversa = ["%i a %i" % (orig, dest) for (orig, dest) in SAtD + SAtI]
            return movi_reg + movi_inversa
        else:
            movi_inversa = ["%i a %i" % (orig, dest) for (orig, dest) in SAdD + SAdI]
            movi_reg = ["%i a %i" % (orig, dest) for (orig, dest) in SAtD + SAtI]
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
        movi_reg = ["%i a %i" % (orig, dest) for (orig, dest) in AdD + AdI]
        movi_inversa = ["%i a %i" % (orig, dest) for (orig, dest) in AtD + AtI]
        return movi_reg + movi_inversa
    else:
        movi_reg = ["%i a %i" % (orig, dest) for (orig, dest) in AtD + AtI]
        movi_inversa = ["%i a %i" % (orig, dest) for (orig, dest) in AdD + AdI]
        return movi_inversa + movi_reg

if __name__ == '__main__':
    try:
        estado= main()
        sys.exit(estado)
    except:
        print ("")
        print ("Juego terminado.")
        sys.exit(1)