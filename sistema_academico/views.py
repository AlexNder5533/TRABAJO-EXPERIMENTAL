from datetime import date
from models.models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.validaciones import es_email_valido

gestor_estudiantes = GestorJSON("data/estudiantes.json")
gestor_materias = GestorJSON("data/materias.json")
gestor_matriculas = GestorJSON("data/matriculas.json")


# Funciones genéricas: trabajan con cualquier modelo y gestor.
def leer_objetos(gestor, modelo):
    return [modelo.desde_diccionario(d) for d in gestor.leer()]


def obtener_por_id(gestor, modelo, id_registro):
    for objeto in leer_objetos(gestor, modelo):
        if objeto.id == int(id_registro):
            return objeto
    return None


def buscar(objetos, termino, campos):
    termino = str(termino).strip().lower()
    encontrados = []
    if not termino:
        return encontrados
    for objeto in objetos:
        texto = " ".join(str(getattr(objeto, campo, "")) for campo in campos).lower()
        if termino in texto:
            encontrados.append(objeto)
    return encontrados


def siguiente_id(gestor):
    # Lista para conservar todos los registros y obtener el mayor identificador.
    registros = gestor.leer()
    return max((int(r.get("id", 0)) for r in registros), default=0) + 1


def guardar_nuevo(gestor, objeto):
    registros = gestor.leer()
    registros.append(objeto.a_diccionario())
    gestor.guardar(registros)


def reemplazar(gestor, objeto):
    registros = gestor.leer()
    for i, registro in enumerate(registros):
        if int(registro["id"]) == objeto.id:
            registros[i] = objeto.a_diccionario()
            gestor.guardar(registros)
            return True
    return False


def eliminar(gestor, id_registro):
    # Comprensión de listas: no se modifica una lista mientras se recorre.
    registros = gestor.leer()
    nuevos = [r for r in registros if int(r["id"]) != int(id_registro)]
    if len(nuevos) == len(registros):
        return False
    gestor.guardar(nuevos)
    return True


def ids_registrados(gestor):
    # Conjunto: comprobar pertenencia evita recorrer repetidamente la lista.
    return {int(r["id"]) for r in gestor.leer()}


def carnets_registrados(excepto_id=None):
    return {r["carnet"].upper() for r in gestor_estudiantes.leer()
            if int(r["id"]) != excepto_id}


def validar_estudiante(datos, id_actual=None):
    obligatorios = ("nombre", "apellido", "email", "carnet", "carrera")
    for campo in obligatorios:
        if not str(datos.get(campo, "")).strip():
            return f"El campo {campo} es obligatorio"
    if not es_email_valido(datos["email"]):
        return "El email no tiene un formato válido"
    carnet = str(datos["carnet"]).strip().upper()
    if carnet in carnets_registrados(id_actual):
        return "El carnet ya está registrado"
    emails = {r["email"].lower() for r in gestor_estudiantes.leer()
              if int(r["id"]) != id_actual}
    if datos["email"].strip().lower() in emails:
        return "El email ya está registrado"
    return None


def crear_estudiante(datos):
    error = validar_estudiante(datos)
    if error:
        return False, error
    estudiante = Estudiante(siguiente_id(gestor_estudiantes), datos["nombre"],
                            datos["apellido"], datos["email"], datos["carnet"],
                            datos["carrera"])
    guardar_nuevo(gestor_estudiantes, estudiante)
    return True, f"Estudiante creado: {estudiante.etiqueta()}"


def obtener_estudiantes():
    return leer_objetos(gestor_estudiantes, Estudiante)


def obtener_estudiante(id_estudiante):
    return obtener_por_id(gestor_estudiantes, Estudiante, id_estudiante)


def buscar_estudiantes(termino):
    # Tupla: campos fijos que se pueden buscar.
    CAMPOS = ("nombre", "apellido", "email", "carnet", "carrera")
    return buscar(obtener_estudiantes(), termino, CAMPOS)


def actualizar_estudiante(id_estudiante, cambios):
    estudiante = obtener_estudiante(id_estudiante)
    if estudiante is None:
        return False, "No existe ese estudiante"
    datos = estudiante.a_diccionario()
    datos.update(cambios)
    error = validar_estudiante(datos, int(id_estudiante))
    if error:
        return False, error
    estudiante.nombre = datos["nombre"].strip()
    estudiante.apellido = datos["apellido"].strip()
    estudiante.email = datos["email"].strip().lower()
    estudiante.carnet = datos["carnet"].strip().upper()
    estudiante.carrera = datos["carrera"].strip()
    reemplazar(gestor_estudiantes, estudiante)
    return True, "Estudiante actualizado"


def eliminar_estudiante(id_estudiante):
    if obtener_estudiante(id_estudiante) is None:
        return False, "No existe ese estudiante"
    if any(m.estudiante_id == int(id_estudiante) for m in obtener_matriculas()):
        return False, "No se puede eliminar: tiene matrículas registradas"
    eliminar(gestor_estudiantes, id_estudiante)
    return True, "Estudiante eliminado"


def validar_materia(datos, id_actual=None):
    for campo in ("nombre", "codigo"):
        if not str(datos.get(campo, "")).strip():
            return f"El campo {campo} es obligatorio"
    if not str(datos.get("creditos", "")).isdigit() or not 1 <= int(datos["creditos"]) <= 10:
        return "Los créditos deben estar entre 1 y 10"
    if not str(datos.get("cupos", "")).isdigit() or not 0 <= int(datos["cupos"]) <= Materia.CUPOS_MAXIMOS:
        return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
    codigo = str(datos["codigo"]).strip().upper()
    codigos = {r["codigo"].upper() for r in gestor_materias.leer()
               if int(r["id"]) != id_actual}
    if codigo in codigos:
        return "El código ya está registrado"
    return None


def crear_materia(datos):
    error = validar_materia(datos)
    if error:
        return False, error
    materia = Materia(siguiente_id(gestor_materias), datos["nombre"], datos["codigo"],
                      datos["creditos"], datos["cupos"])
    guardar_nuevo(gestor_materias, materia)
    return True, f"Materia creada: {materia.etiqueta()}"


def obtener_materias():
    return leer_objetos(gestor_materias, Materia)


def obtener_materia(id_materia):
    return obtener_por_id(gestor_materias, Materia, id_materia)


def buscar_materias(termino):
    CAMPOS = ("nombre", "codigo")
    return buscar(obtener_materias(), termino, CAMPOS)


def actualizar_materia(id_materia, cambios):
    materia = obtener_materia(id_materia)
    if materia is None:
        return False, "No existe esa materia"
    datos = materia.a_diccionario()
    datos.update(cambios)
    error = validar_materia(datos, int(id_materia))
    if error:
        return False, error
    # No permitir reducir cupos por debajo de matrículas activas ya realizadas.
    usados = sum(1 for m in obtener_matriculas() if m.materia_id == materia.id)
    if int(datos["cupos"]) + usados > Materia.CUPOS_MAXIMOS:
        return False, "Los cupos más las matrículas existentes superan el máximo"
    materia.nombre = datos["nombre"].strip()
    materia.codigo = datos["codigo"].strip().upper()
    materia.creditos = int(datos["creditos"])
    materia.cupos = int(datos["cupos"])
    reemplazar(gestor_materias, materia)
    return True, "Materia actualizada"


def eliminar_materia(id_materia):
    if obtener_materia(id_materia) is None:
        return False, "No existe esa materia"
    if any(m.materia_id == int(id_materia) for m in obtener_matriculas()):
        return False, "No se puede eliminar: tiene matrículas registradas"
    eliminar(gestor_materias, id_materia)
    return True, "Materia eliminada"


def materias_sin_cupo():
    return [m for m in obtener_materias() if not m.hay_cupo()]


def obtener_matriculas():
    return leer_objetos(gestor_matriculas, Matricula)


def obtener_matricula(id_matricula):
    return obtener_por_id(gestor_matriculas, Matricula, id_matricula)


def crear_matricula(datos):
    estudiante = obtener_estudiante(datos.get("estudiante_id"))
    materia = obtener_materia(datos.get("materia_id"))
    if estudiante is None:
        return False, "El estudiante no existe"
    if materia is None:
        return False, "La materia no existe"
    if not materia.hay_cupo():
        return False, "La materia no tiene cupos disponibles"
    periodo = str(datos.get("periodo", "")).strip()
    if not periodo:
        return False, "El periodo es obligatorio"
    # Conjunto de tuplas: evita duplicar estudiante + materia + periodo.
    claves = {(m.estudiante_id, m.materia_id, m.periodo) for m in obtener_matriculas()}
    if (estudiante.id, materia.id, periodo) in claves:
        return False, "El estudiante ya está matriculado en esa materia y periodo"
    matricula = Matricula(siguiente_id(gestor_matriculas), estudiante.id,
                          materia.id, periodo, 0, date.today().isoformat())
    guardar_nuevo(gestor_matriculas, matricula)
    materia.ocupar_cupo()
    reemplazar(gestor_materias, materia)
    return True, f"Matrícula creada con id {matricula.id}"


def registrar_nota(id_matricula, nota):
    matricula = obtener_matricula(id_matricula)
    if matricula is None:
        return False, "No existe esa matrícula"
    if not Materia.es_nota_valida(nota):
        return False, "La nota debe ser un número entre 0 y 20"
    matricula.nota = float(nota)
    reemplazar(gestor_matriculas, matricula)
    return True, f"Nota registrada. Estado: {matricula.estado()}"


def retirar_matricula(id_matricula):
    matricula = obtener_matricula(id_matricula)
    if matricula is None:
        return False, "No existe esa matrícula"
    materia = obtener_materia(matricula.materia_id)
    if materia is not None:
        materia.liberar_cupo()
        reemplazar(gestor_materias, materia)
    eliminar(gestor_matriculas, id_matricula)
    return True, "Matrícula retirada y cupo liberado"


def certificado(id_matricula):
    matricula = obtener_matricula(id_matricula)
    if matricula is None:
        return None
    # Diccionarios índice {id: objeto}: acceso directo a estudiante y materia.
    estudiantes = {e.id: e for e in obtener_estudiantes()}
    materias = {m.id: m for m in obtener_materias()}
    estudiante = estudiantes.get(matricula.estudiante_id)
    materia = materias.get(matricula.materia_id)
    if estudiante is None or materia is None:
        return None
    return {
        "matricula": matricula,
        "estudiante": estudiante,
        "materia": materia
    }


def matriculas_por_estudiante():
    # Diccionario de listas: agrupa varias matrículas bajo el id de estudiante.
    agrupadas = {}
    for matricula in obtener_matriculas():
        agrupadas.setdefault(matricula.estudiante_id, []).append(matricula)
    return agrupadas


def promedio_de_estudiante(id_estudiante):
    notas = [m.nota for m in obtener_matriculas()
             if m.estudiante_id == int(id_estudiante)]
    if not notas:
        return None
    return round(sum(notas) / len(notas), 2)


def resumen():
    estudiantes = obtener_estudiantes()
    carreras = sorted({e.carrera for e in estudiantes})
    aprobadas = sum(1 for m in obtener_matriculas() if m.esta_aprobada())
    return {
        "estudiantes": len(estudiantes),
        "carreras": carreras,
        "materias_sin_cupo": materias_sin_cupo(),
        "matriculas_aprobadas": aprobadas
    }
