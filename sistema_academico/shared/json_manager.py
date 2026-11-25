import json
import os


class GestorJSON:
    def __init__(self, archivo):
        self.archivo = archivo
        carpeta = os.path.dirname(archivo)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        if not os.path.exists(self.archivo):
            self.guardar([])

    def leer(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        temporal = self.archivo + ".tmp"
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        os.replace(temporal, self.archivo)
