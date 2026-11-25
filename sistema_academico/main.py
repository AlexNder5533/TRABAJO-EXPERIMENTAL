import views


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_id(texto="Ingrese el ID: "):
    try:
        return int(input(texto))
    except ValueError:
        print("El ID debe ser un número entero.")
        return None


def mostrar_lista(objetos):
    if not objetos:
        print("\nNo hay registros.")
        return
    for objeto in objetos:
        print(f"  {objeto}")


def mostrar_detalle(objeto):
    if objeto is None:
        print("No se encontró el registro.")
    else:
        print(objeto)
        for clave, valor in objeto.a_diccionario().items():
            print(f"  {clave}: {valor}")


def menu_crud(tipo):
    es_estudiante = tipo == "estudiantes"
    nombre = "Estudiantes" if es_estudiante else "Materias"
    obtener = views.obtener_estudiantes if es_estudiante else views.obtener_materias
    crear = views.crear_estudiante if es_estudiante else views.crear_materia
    buscar = views.buscar_estudiantes if es_estudiante else views.buscar_materias
    obtener_uno = views.obtener_estudiante if es_estudiante else views.obtener_materia
    actualizar = views.actualizar_estudiante if es_estudiante else views.actualizar_materia
    eliminar = views.eliminar_estudiante if es_estudiante else views.eliminar_materia

    while True:
        print(f"\n--- {nombre.upper()} ---")
        print("1. Crear")
        print("2. Ver todos")
        print("3. Buscar")
        print("4. Ver por ID")
        print("5. Actualizar")
        print("6. Eliminar")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            if es_estudiante:
                datos = {
                    "nombre": input("Nombre: "),
                    "apellido": input("Apellido: "),
                    "email": input("Email: "),
                    "carnet": input("Carnet: "),
                    "carrera": input("Carrera: ")
                }
            else:
                datos = {
                    "nombre": input("Nombre de la materia: "),
                    "codigo": input("Código: "),
                    "creditos": input("Créditos (1-10): "),
                    "cupos": input("Cupos iniciales (0-30): ")
                }
            exito, mensaje = crear(datos)
            print(mensaje)

        elif opcion == "2":
            mostrar_lista(obtener())

        elif opcion == "3":
            mostrar_lista(buscar(input("Texto a buscar: ")))

        elif opcion == "4":
            id_registro = pedir_id()
            if id_registro is not None:
                mostrar_detalle(obtener_uno(id_registro))

        elif opcion == "5":
            id_registro = pedir_id()
            if id_registro is None:
                continue
            if obtener_uno(id_registro) is None:
                print("No existe ese registro.")
                continue
            print("Deje vacío lo que no desea cambiar.")
            if es_estudiante:
                cambios = {}
                for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
                    valor = input(f"{campo.capitalize()}: ").strip()
                    if valor:
                        cambios[campo] = valor
            else:
                cambios = {}
                for campo in ("nombre", "codigo", "creditos", "cupos"):
                    valor = input(f"{campo.capitalize()}: ").strip()
                    if valor:
                        cambios[campo] = valor
            if not cambios:
                print("No indicó ningún cambio.")
            else:
                exito, mensaje = actualizar(id_registro, cambios)
                print(mensaje)

        elif opcion == "6":
            id_registro = pedir_id()
            if id_registro is not None:
                exito, mensaje = eliminar(id_registro)
                print(mensaje)

        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
        pausa()


def menu_matriculas():
    while True:
        print("\n--- MATRÍCULAS ---")
        print("1. Matricular")
        print("2. Ver todas")
        print("3. Registrar nota")
        print("4. Ver certificado")
        print("5. Retirar matrícula")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            datos = {
                "estudiante_id": pedir_id("ID del estudiante: "),
                "materia_id": pedir_id("ID de la materia: "),
                "periodo": input("Periodo (ej. 2026-1): ")
            }
            if None in (datos["estudiante_id"], datos["materia_id"]):
                print("No se pudo registrar la matrícula.")
            else:
                exito, mensaje = views.crear_matricula(datos)
                print(mensaje)

        elif opcion == "2":
            mostrar_lista(views.obtener_matriculas())

        elif opcion == "3":
            id_matricula = pedir_id("ID de la matrícula: ")
            if id_matricula is not None:
                nota = input("Nota (0-20): ")
                exito, mensaje = views.registrar_nota(id_matricula, nota)
                print(mensaje)

        elif opcion == "4":
            id_matricula = pedir_id("ID de la matrícula: ")
            if id_matricula is not None:
                datos = views.certificado(id_matricula)
                if datos is None:
                    print("No se encontró el certificado.")
                else:
                    m = datos["matricula"]
                    e = datos["estudiante"]
                    materia = datos["materia"]
                    print(f"\nCERTIFICADO #{m.id}   periodo: {m.periodo}")
                    print(f"Estudiante: {e.nombre_completo()} ({e.carnet})")
                    print(f"Materia   : {materia.nombre} ({materia.codigo}) · {materia.creditos} créditos")
                    print("------------------------------------------")
                    print(f"Nota      : {m.nota:.1f}")
                    print(f"Estado    : {m.estado()}")

        elif opcion == "5":
            id_matricula = pedir_id("ID de la matrícula: ")
            if id_matricula is not None:
                exito, mensaje = views.retirar_matricula(id_matricula)
                print(mensaje)

        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
        pausa()


def mostrar_resumen():
    datos = views.resumen()
    print("\n--- RESUMEN ACADÉMICO ---")
    print(f"Cantidad de estudiantes: {datos['estudiantes']}")
    print("Carreras distintas:", ", ".join(datos["carreras"]) if datos["carreras"] else "Ninguna")
    print("Materias sin cupo:")
    mostrar_lista(datos["materias_sin_cupo"])
    print(f"Matrículas aprobadas: {datos['matriculas_aprobadas']}")


def main():
    while True:
        print("\n========== SISTEMA ACADÉMICO ==========")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Matrículas")
        print("4. Resumen")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_crud("estudiantes")
        elif opcion == "2":
            menu_crud("materias")
        elif opcion == "3":
            menu_matriculas()
        elif opcion == "4":
            mostrar_resumen()
            pausa()
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
