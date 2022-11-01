import datetime
import sqlite3
from sqlite3 import Error
import sys

fecha_consultar = input("Fecha que desea consultar (dd/mm/aaaa): ")
fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()

try:
    with sqlite3.connect("evidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        mi_cursor = conn.cursor()
        criterios = {"fecha":fecha_consultar}
        mi_cursor.execute("SELECT id_sala, nombre, cupo, nombret FROM sala, turno, reservas WHERE DATE(fecha_registro) = :fecha AND fechar= NULL;", criterios)
        registros = mi_cursor.fetchall()
   
        for id_sala, nombre, cupo in registros:
            print(f"id_sala = {id_sala}")
            print(f"Nombre = {nombre}")
            print(f"cupo = {cupo}\n")
        
except sqlite3.Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")
