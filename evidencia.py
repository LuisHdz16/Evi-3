import datetime
import sys
import sqlite3
from sqlite3 import Error
import openpyxl
import os

if os.path.isfile("evidencia3.db"):
    print("\nSe detecto que hay datos previos.")
else:
    try:
        with sqlite3.connect("evidencia3.db") as conn_creacion_tablas:
            mi_cursor = conn_creacion_tablas.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS salas (id_sala INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, cupo INTEGER NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS turnos (id_turno INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS reservas (folio INTEGER PRIMARY KEY AUTOINCREMENT, fecha TIMESTAMP,id_cliente INTEGER NOT NULL, id_sala INTEGER NOT NULL, nombre_evento TEXT NOT NULL, id_turno INTEGER NOT NULL, FOREIGN KEY(id_cliente) REFERENCES CLIENTES(id_cliente), FOREIGN KEY(id_sala) REFERENCES salas(id_sala), FOREIGN KEY(id_turno) REFERENCES turnos(id_turno));")
            mi_cursor.execute("INSERT INTO turnos (nombre) VALUES('Matutino')")
            mi_cursor.execute("INSERT INTO turnos (nombre) VALUES('Vespertino')")
            mi_cursor.execute("INSERT INTO turnos (nombre) VALUES('Nocturno')")
            print("\nEs la primera vez que se ejecuta el programa.")
        conn_creacion_tablas.close()
    except Error as e:
        print(e)

while True:

    print("""
    --------------------------------MENÚ PRINCIPAL--------------------------------\n
    [A] RESERVACIONES.\n
    [B] REPORTES.\n
    [C] REGISTRAR NUEVO CLIENTE.\n
    [D] REGISTRAR NUEVA SALA.\n
    [E] Salir
    """)

    opcion_menu = input("Seleccione una opción: ")

    if opcion_menu.upper() == "A":

        while True:

            print("""
    --------------------------------MENÚ RESERVAS--------------------------------\n
    [A] REGISTRAR NUEVA RESERVACIÓN\n
    [B] MODIFICAR DESCRIPCION DE UNA RESERVACIÓN\n
    [C] CONSULTAR DISPONIBIBLIDAD DE SALAS PARA UNA FECHA\n
    [D] ELIMINAR UNA RESERVACIÓN\n
    [E] VOLVER AL MENÚ PRINCIPAL
    """)

            opcion_menu_reservas = input("Elija una opción: ")

            if opcion_menu_reservas.upper() == "A":
                pass
            elif opcion_menu_reservas.upper() == "B":
                pass
            elif opcion_menu_reservas.upper() == "C":
                pass
            elif opcion_menu_reservas.upper() == "D":
                pass
            elif opcion_menu_reservas.upper() == "E":
                break
            else:
                print("\nElija una opcion correcta.")
    elif opcion_menu.upper() == "B":
        
        while True:

            print("""
    --------------------------------MENÚ REPORTES--------------------------------\n
    [A] REPORTE EN PANTALLA DE RESERVACIONES PARA UNA FECHA\n
    [B] EXPORTAR REPORTE TABULAR EN EXCEL\n
    [C] VOLVER AL MENÚ PRINCIPAL\n
    """)

            opcion_menu_reportes = input("\nElija una opción: ")

            if opcion_menu_reportes.upper() == "A":
                pass
            elif opcion_menu_reportes.upper() == "B":
                pass
            elif opcion_menu_reportes.upper() == "C":
                break
            else:
                print("\nElija una opcion correcta.")
    elif opcion_menu.upper() == "C":
        pass
    elif opcion_menu.upper() == "D":
        pass
    elif opcion_menu.upper() == "E":
        break
    else:
        print("\nElija una opcion correcta.")

