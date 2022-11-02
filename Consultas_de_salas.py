elif opcion_menu_reservas.upper() == "C":
                while True:
                    listas_ocupadas = list()
                    lista_posibles = list()

                    fecha_para_ver_disponibles_capturada = input("\nIngrese la fecha donde quiera ver la disponibilidad: ")

                    if fecha_para_ver_disponibles_capturada.strip() == "":
                        print("\nLa fecha no puede omitise.")
                        continue

                    try:
                        fecha_para_ver_disponibles = datetime.datetime.strptime(fecha_para_ver_disponibles_capturada, "%d/%m/%Y").date()
                    except Exception:
                        print("\nFormato de fecha incorrecto.")
                        continue
                    
                    try:
                        with sqlite3.connect("evidencia3.db") as conn_disponibilidad:
                            mi_cursor = conn_disponibilidad.cursor()
                            fechaDis_ = fecha_para_ver_disponibles_capturada.strftime("%d/%m/%Y"),
                            mi_cursor.execute(f"SELECT id_sala, nombre, id_turno FROM reservas WHERE fecha=?", fechaDis_)
                            registros_reservas_disponibilidad = mi_cursor.fetchall()
                        conn_disponibilidad.close()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                    for id_sala, nombre, id_turno in listas_ocupadas:
                        try:
                            with sqlite3.connect("evidencia3.db") as conn_salas_disponibilidad:
                                mi_cursor = conn_salas_disponibilidad.cursor()           
                                mi_cursor.execute(f"SELECT id_sala, nombre FROM salas WHERE id_sala={id_sala}")
                                salas_reservas_disponibilidad = mi_cursor.fetchall()
                            conn_salas_disponibilidad.close()
                        except Error as e:
                            print(e)
                        except Exception:
                            print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                        try:
                            with sqlite3.connect("evidencia3.db") as conn_turnos_disponibilidad:
                                mi_cursor = conn_turnos_disponibilidad.cursor()
                                mi_cursor.execute(f"SELECT nombre FROM turnos WHERE id_turno={id_turno}")
                                turnos_reservas_disponibilidad = mi_cursor.fetchall()
                            conn_turnos_disponibilidad.close()
                        except Error as e:
                            print(e)
                        except Exception:
                            print(f"\nSe produjo el siguiente error: {sys.exc_info()[0]}")

                    reservas_ocupadas = set(listas_ocupadas)

                    for sala in salas_dict:
                        for turno in turno_dict:
                            lista_posibles.append((salas_reservas_disponibilidad, turnos_reservas_disponibilidad[turno]))
                    
                    reservas_posibles = set(lista_posibles)

                    reservaciones_disponibles = sorted(list(reservas_posibles - reservas_ocupadas))

                    print(f"\n** Salas disponibles para renta el {fecha_para_ver_disponibles_capturada} **")
                    print(f"\n{'SALA':<20}{'TURNO':>20}")
                    for sala, turno in reservaciones_disponibles:
                        print(f"{sala},{salas_dict[sala][0]:<20}{turno:>20}")
                    break
