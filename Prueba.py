import Tablero
import IA_Damas
import IA
import IA_Damas_Random

NEGRO, BLANCO = 0, 1

f = open('logfile', 'w')

for i in range(100):
    print ("Juego: " + str(i))
    B = Tablero.TableroDamas()
    cpu_1 = IA_Damas.IA_Damas(lambda Tablero: IA.funcion_de_movimiento(Tablero, 4))
    cpu_2 = IA_Damas.IA_Damas(lambda Tablero: IA.funcion_de_movimiento(Tablero, 6))
    jugador_actual = B.activo
    Turno = 1
    while not B.se_termino():
        f.write(str(B))
        if Turno % 100 == 0:
            print ("Numero de Turnos: " + str(Turno))
        B.hacer_movi(cpu_1.hacer_movi(B))
        if B.activo == jugador_actual:
            continue
        jugador_actual = B.activo
        Turno += 1
        while not B.se_termino() and B.activo == jugador_actual:
            B.hacer_movi(cpu_2.hacer_movi(B))
        jugador_actual = B.activo
    if B.activo == BLANCO:
        print ("Gano negro!")
    else:
        print ("Gano blanco!")
    print ("juego tardo %i Turnos" % Turno)