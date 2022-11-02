# Este deberia mostrar todo lo que hay en el select pero por fecha pero no consegui pasar el str a formato fecha
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
        mi_cursor.execute("SELECT folio, fechar, id_cliente, id_sala, nombre_evento, id_turno FROM reservas WHERE fechar = :fecha;", criterios)
        registros = mi_cursor.fetchall()
   
        for folio, fechar, id_cliente, id_sala, nombre_evento, id_turno in registros:
            print(f"folio = {folio}")
            print(f"fechar = {fechar.date()}, tipo de dato {type(fechar)}")
            print(f"nombre_evento = {nombre_evento}")
            print(f"id_sala = {id_sala}")
            print(f"id_turno = {id_turno}")
            print(f"id_cliente = {id_cliente}\n")
        
except sqlite3.Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")
