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

clientes_dict = dict()
salas_dict = dict()
reservas_dict = dict()
turno_dict = {1: "Matutino", 2: "Vespertino", 3: "Nocturno"}

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
                while True:

                    try:
                        with sqlite3.connect("evidencia3.db") as conn_mostrar_clientes:
                            cursor = conn_mostrar_clientes.cursor()
                            cursor.execute("SELECT id_cliente, nombre FROM clientes")
                            registros_clientes_mostrar = cursor.fetchall()
                            print(f"\n{'Clientes registrados':^40}")
                            print("-" * 40)
                            print("Clave\t\tCliente")
                            print("-" * 40)
                            for clave, nombre in registros_clientes_mostrar:
                                print(f"{clave}\t\t{nombre}")
                            print("-" * 40)
                        conn_mostrar_clientes.close()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                    reserva_clave_del_cliente_capturada = input("\nIngresa la clave del cliente: ")

                    if reserva_clave_del_cliente_capturada.strip() == "":
                        print("\nLa clave del cliente no puede omitirse. Intente de nuevo.")
                        continue

                    reserva_clave_del_cliente = puede_ser_int(reserva_clave_del_cliente_capturada)

                    try:
                        with sqlite3.connect("evidencia3.db") as conn_clientes_select_id:
                            mi_cursor = conn_clientes_select_id.cursor()
                            mi_cursor.execute(f"SELECT  nombre FROM clientes WHERE id_cliente={reserva_clave_del_cliente}")
                            clientes_registros_id = mi_cursor.fetchall()
                        conn_clientes_select_id.close()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

                    if clientes_registros_id:
                        print(f"\nCliente {clientes_registros_id[0][0]} puede continuar con la resevación.")
                        break
                    else:
                        print("\nNo se encontro la clave del cliente.")
                        continue

                while True:
                    
                    try:
                        with sqlite3.connect("evidencia3.db")as conn_salas_mostrar:
                            mi_cursor = conn_salas_mostrar.cursor()
                            mi_cursor.execute("SELECT id_sala, nombre, cupo FROM salas")
                            registros_salas = mi_cursor.fetchall()
                            print(f"\n{'Salas registrados':^40}")
                            print("-" * 40)
                            print(f"{'Clave':<10}{'Nombre':<25}{'Cupo'}")
                            print("-" * 40)
                            for clave, nombre, cupo in registros_salas:
                                print(f"{clave:<10}{nombre:<25}{cupo}")
                            print("-" * 40)
                        conn_salas_mostrar.close()  
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                    clave_de_sala_reservas_capturada = input("\nIngresa el número de sala: ")

                    if clave_de_sala_reservas_capturada.strip() == "":
                        print("\nEl número de sala no puede omitirse.")
                        continue

                    clave_de_sala_reservas = puede_ser_int(clave_de_sala_reservas_capturada)

                    if clave_de_sala_reservas == False:
                        print("\nEl dato proporcionado no es de tipo entero.")
                        continue

                    try:
                        with sqlite3.connect("evidencia3.db")as conn_salas_mostrar_por_id:
                            mi_cursor = conn_salas_mostrar_por_id.cursor()
                            mi_cursor.execute(f"SELECT nombre, cupo FROM salas WHERE id_sala={clave_de_sala_reservas}")
                            registro_sala_por_id = mi_cursor.fetchall()
                        conn_salas_mostrar_por_id.close()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                    if registro_sala_por_id:
                        print(f"\nSala {registro_sala_por_id[0][0]} seleccionada.")
                        break
                    else:
                        print("\nNo se encontro la clave de la sala.")
                        continue

                while True:

                    fecha_actual = datetime.date.today()

                    fecha_reservacion_capturada = input("\nEscribe la fecha de reservación que desea con el formato dd/mm/aaaa: ")

                    if fecha_reservacion_capturada.strip() == "":
                        print("\nEl dato proporcionado no es de tipo entero.")
                        continue

                    fecha_reservacion = puede_ser_tipo_fecha(fecha_reservacion_capturada)

                    if fecha_reservacion == False:
                        print("\nEl dato proporcionado no es de tipo entero.")
                        continue

                    resta_fecha = fecha_reservacion - fecha_actual

                    if resta_fecha.days < 2 and resta_fecha.days >= 0:
                        print("\nLa reservación debe hacerse dos días antes del día elegido.")
                        continue
                    elif resta_fecha.days < 0:
                        print("\nEsa fecha ya pasó.")
                        continue
                    
                    break

                while True:

                    try:
                        with sqlite3.connect("evidencia3.db")as conn_turnos_mostrar:
                            mi_cursor = conn_turnos_mostrar.cursor()
                            mi_cursor.execute("SELECT id_turno, nombre FROM turnos")
                            registros_turnos = mi_cursor.fetchall()
                            print(f"\n{'Turnos posibles':^40}")
                            print("-" * 40)
                            print("Clave\t\tTurno")
                            print("-" * 40)
                            for clave, turno in registros_turnos:
                                print(f"{clave}\t\t{turno}")
                            print("-" * 40)
                        conn_turnos_mostrar.close()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")
                                        
                    turno_reservacion_capturada = input("\nElija un turno por su clave: ")

                    if turno_reservacion_capturada.strip() == "":
                        print("\nEl turno no puede omitirse.")
                        continue
                    
                    turno_reservacion = puede_ser_int(turno_reservacion_capturada)

                    if turno_reservacion == False:
                        print("\nEl dato proporcionado no es de tipo entero.")
                        continue
                    
                    try:
                        with sqlite3.connect("evidencia3.db")as conn_turno_por_id:
                            mi_cursor = conn_turno_por_id.cursor()
                            mi_cursor.execute(f"SELECT nombre FROM turnos WHERE id_turno={turno_reservacion}")
                            registros_turnos_por_id = mi_cursor.fetchall()
                        conn_turno_por_id.close()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                    if registros_turnos_por_id:
                        print(f"\nTurno {registros_turnos_por_id[0][0]} seleccionada.")
                        break
                    else:
                        print("\nNo se encontro la clave del turno.")
                        continue

                while True:
                                    
                    try:
                        with sqlite3.connect("evidencia3.db")as conn_reservas_mostrar:
                            mi_cursor = conn_reservas_mostrar.cursor()
                            mi_cursor.execute("SELECT folio, fecha, id_cliente, id_sala, nombre_evento ,id_turno FROM reservas")
                            registros_reservas = mi_cursor.fetchall()
                        conn_reservas_mostrar.close()
                    except Error as e:
                        print (e)
                    except Exception:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

                    for folio, fecha, id_cliente, id_sala, nombre_evento ,id_turno in registros_reservas:
                        if fecha_reservacion.strftime("%d/%m/%Y") == fecha and clave_de_sala_reservas == id_sala and turno_reservacion == id_turno:
                            print(f"\nEstá ocupada esa sala y turno en la fecha {fecha_reservacion_capturada}.")
                            break
                    else:

                        while True:

                            nombre_evento = input("\nIngrese el nombre del evento: ")

                            if nombre_evento.strip() == "":
                                print("\nEl nombre no puede omitirse.")
                                continue

                            break
                        try:
                            with sqlite3.connect("evidencia3.db")as conn_reservas:
                                mi_cursor = conn_reservas.cursor()
                                insert_reservas = (fecha_reservacion.strftime("%d/%m/%Y"), reserva_clave_del_cliente, clave_de_sala_reservas, nombre_evento, turno_reservacion)
                                mi_cursor.execute("INSERT INTO reservas (fecha, id_cliente, id_sala, nombre_evento ,id_turno) VALUES (?,?,?,?,?)", insert_reservas)
                                print("\nReservacion completada correctamente.")
                            conn_reservas.close()      
                        except Error as e:
                            print (e)
                        except Exception:
                            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                    break
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
        while True:

            cliente_nombre = input("\nIngresa el nombre del cliente: ")

            if cliente_nombre.strip() == "":
                print("\nEl nombre no se puede omitir.")
                continue
            try:
                with sqlite3.connect("evidencia3.db") as conn_clientes_insert:
                    mi_cursor = conn_clientes_insert.cursor()
                    cliente_nombre_insert = {"nombre":cliente_nombre}
                    mi_cursor.execute("INSERT INTO clientes (nombre) VALUES(:nombre)", cliente_nombre_insert)
                    print("\nSe registro el cliente exitosamente")
                conn_clientes_insert.close()
            except Error as e:
                print(e)
            except:
                print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")
            break
    elif opcion_menu.upper() == "D":
        while True:

            sala_nombre = input("\nIngrese el nombre de sala: ")

            if sala_nombre.strip() == "":
                print("\nNo puede omitirse el nombre de la sala. Intente de nuevo.")
                continue

            break

        while True:

            sala_cupo_capturado = input("\nCupo de la sala: ")

            if sala_cupo_capturado.strip() == "":
                print("\nNo puede omitirse el cupo de la sala.")
                continue

            sala_cupo = puede_ser_int(sala_cupo_capturado)

            if sala_cupo == False:
                print("\nEl dato proporcionado no es de tipo entero.")
                continue
            
            if sala_cupo <= 0:
                print("\nEl cupo de la sala debe ser mayor a cero.")
                continue

            try:
                with sqlite3.connect("evidencia3.db") as conn_salas_insert:
                    mi_cursor = conn_salas_insert.cursor()
                    sala_insert = {"nombre":sala_nombre, "cupo":sala_cupo}
                    mi_cursor.execute("INSERT INTO salas (nombre, cupo) VALUES(:nombre, :cupo)", sala_insert)
                    print("\nSe registro la sala exitosamente")
                conn_salas_insert.close()
            except Error as e:
                print (e)
            except:
                print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

            break
    elif opcion_menu.upper() == "E":
        break
    else:
        print("\nElija una opcion correcta.")
