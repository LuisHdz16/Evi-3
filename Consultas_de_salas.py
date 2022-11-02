# Este es para ver las salas con la combinacion de cada turno
from datetime import date, datetime
import sqlite3
from sqlite3 import Error
import sys

try:
    with sqlite3.connect("evidencia3.db") as conn:
        mi_cursor = conn.cursor()
        mi_cursor.execute("SELECT id_sala, nombre, nombret, cupo FROM salas, turnos")
        registros = mi_cursor.fetchall()
   
        for id_sala, nombre, nombret, cupo in registros:
            print(f"id_sala = {id_sala}")
            print(f"nombre = {nombre}")
            print(f"nombret = {nombret}")
            print(f"cupo = {cupo}\n")
        
except sqlite3.Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")
