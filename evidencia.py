import datetime
import sys
import sqlite3
from sqlite3 import Error
import openpyxl
import os

def puede_ser_tipo_fecha(fecha):
    try:
        return datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
    except Exception:
        return False

def puede_ser_int(valor):
    try:
        return int(valor)
    except Exception:
        return False

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

consulta_reservaciones = []

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
                while True:

                    consulta_reservaciones.clear()

                    fecha_a_consultar_capturada = input("\nFecha que desea consultar si hay reservaciones: ")

                    if fecha_a_consultar_capturada.strip() == "":
                        print("\nNo se puede omitir la fecha.")
                        continue
                    
                    fecha_a_consultar = puede_ser_tipo_fecha(fecha_a_consultar_capturada)

                    if fecha_a_consultar == False:
                        print("\nNo es de tipo de fecha correcto.")
                        continue

                    try:
                        with sqlite3.connect("evidencia3.db") as conn_reservas_reporte:
                            mi_cursor = conn_reservas_reporte.cursor()
                            fecha_ = fecha_a_consultar.strftime("%d/%m/%Y"),
                            mi_cursor.execute(f"SELECT id_sala, id_cliente, nombre_evento ,id_turno FROM reservas WHERE fecha=?", fecha_)
                            registros_reservas_reporte = mi_cursor.fetchall()
                        conn_reservas_reporte.close()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                        

                    for id_sala, id_cliente, nombre_evento, id_turno in registros_reservas_reporte:
                        try:
                            with sqlite3.connect("evidencia3.db") as conn_clientes_reporte:
                                mi_cursor = conn_clientes_reporte.cursor()
                                mi_cursor.execute(f"SELECT  nombre FROM clientes WHERE id_cliente={id_cliente}")
                                cliente_nombre_reporte = mi_cursor.fetchall()
                            conn_clientes_reporte.close()
                        except Error as e:
                            print(e)
                        except Exception:
                            print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                        try:
                            with sqlite3.connect("evidencia3.db")as conn_turnos_reporte:
                                mi_cursor = conn_turnos_reporte.cursor()
                                mi_cursor.execute(f"SELECT nombre FROM turnos WHERE id_turno={id_turno}")
                                turno_nombre_reporte = mi_cursor.fetchall()
                            conn_turnos_reporte.close()
                        except Error as e:
                            print(e)
                        except Exception:
                            print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                        consulta_reservaciones.append((id_sala, cliente_nombre_reporte[0][0], nombre_evento, turno_nombre_reporte[0][0]))
                        continue
                            
                    if len(consulta_reservaciones) == 0:
                        print("\nNo hay reservaciones en esa fecha.")
                        break

                    print("*" * 100)
                    print(f"{'REPORTE DE RESERVACIONES PARA EL DIA ' + fecha_a_consultar_capturada:^100}")
                    print("*" * 100)
                    print(f"{'SALA':<15}{'CLIENTE':<20}{'EVENTO':<50}TURNO")
                    print("*" * 100)
                    for datos in consulta_reservaciones:
                        print(f"{datos[0]:<15}{datos[1]:<20}{datos[2]:<50}{datos[3]}")
                    print("*" * 100)
                    break
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