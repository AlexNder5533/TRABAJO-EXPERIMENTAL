class ModeloBase:
    def __init__(self, id_registro):
        self.id = int(id_registro)

    @classmethod
    def desde_diccionario(cls, datos):
        datos = datos.copy()
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        return str(self.id)

    def __str__(self):
        return f"[{self.id}] {self.etiqueta()}"


class Persona(ModeloBase):
    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = str(nombre).strip()
        self.apellido = str(apellido).strip()
        self.email = str(email).strip().lower()

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email
        })
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Estudiante(Persona):
    def __init__(self, id_registro, nombre, apellido, email, carnet="", carrera=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = str(carnet).strip().upper()
        self.carrera = str(carrera).strip()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · {self.carnet} · {self.carrera}"


class Materia(ModeloBase):
    CUPOS_MAXIMOS = 30
    NOTA_APROBACION = 14

    def __init__(self, id_registro, nombre, codigo, creditos=0, cupos=0):
        super().__init__(id_registro)
        self.nombre = str(nombre).strip()
        self.codigo = str(codigo).strip().upper()
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    @staticmethod
    def es_nota_valida(valor):
        try:
            nota = float(valor)
            return 0 <= nota <= 20
        except (TypeError, ValueError):
            return False

    def hay_cupo(self):
        return self.cupos > 0

    def ocupar_cupo(self):
        if self.hay_cupo():
            self.cupos -= 1
            return True
        return False

    def liberar_cupo(self):
        if self.cupos < self.CUPOS_MAXIMOS:
            self.cupos += 1
            return True
        return False

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "nombre": self.nombre,
            "codigo": self.codigo,
            "creditos": self.creditos,
            "cupos": self.cupos
        })
        return datos

    def etiqueta(self):
        alerta = " · SIN CUPO" if not self.hay_cupo() else ""
        return f"{self.nombre} · {self.codigo} · {self.creditos} créditos · {self.cupos} cupos{alerta}"


class Matricula(ModeloBase):
    def __init__(self, id_registro, estudiante_id, materia_id, periodo, nota=0, fecha=""):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = str(periodo).strip()
        self.nota = float(nota)
        self.fecha = str(fecha).strip()

    def esta_aprobada(self):
        return self.nota >= Materia.NOTA_APROBACION

    def estado(self):
        return "Aprobado" if self.esta_aprobada() else "Reprobado"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "estudiante_id": self.estudiante_id,
            "materia_id": self.materia_id,
            "periodo": self.periodo,
            "nota": self.nota,
            "fecha": self.fecha
        })
        return datos

    def etiqueta(self):
        return f"Estudiante {self.estudiante_id} · Materia {self.materia_id} · {self.periodo} · {self.nota:.1f} ({self.estado()})"
