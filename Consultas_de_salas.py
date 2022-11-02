# Este me da en teoria las que estan disponibles pero tuve que poner una columna en reservas llamada nombre porque no me dejaba unirla con la de salas, 
# me salia que era ambiguo el nombre (id_sala) asi que puse la columna solo para probarlo, faltaria la restriccion de que no agarre los que ya tienen reserva pero 
# no se del todo como podria hacerlo
import datetime
import sqlite3
from sqlite3 import Error
import sys

fecha_consultar = input("Dime una fecha (dd/mm/aaaa): ")
fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()

try:
    with sqlite3.connect("evidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        mi_cursor = conn.cursor()
        valores = {"fechar":fecha_consultar}
        mi_cursor.execute("SELECT id_sala, nombre, nombret, fecha FROM reservas, turnos WHERE DATE(fecha) = :fechar;", valores)
        registros = mi_cursor.fetchall()
   
        if registros:
            for id_sala, nombre, nombret, fecha in registros:
                  print(f"ID_Sala = {id_sala}")
                  print(f"Turno = {nombret}")
                  print(f"Sala = {nombre}")
                  print(f"Fecha = {fecha.date().strftime('%d/%m/%Y')}, tipo de dato {type(fecha)}\n")
        else:
            print(f"No se encontró salas disponibles asociadas con la fecha {fecha_consultar}")
        
except sqlite3.Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")
