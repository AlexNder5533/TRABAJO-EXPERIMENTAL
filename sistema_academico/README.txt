SISTEMA ACADÉMICO - CRUD EN PYTHON CON MVC

Requisitos:
- Python 3.9 o superior.
- No requiere instalar librerías externas.

Ejecución:
1. Descomprima el ZIP.
2. Abra la carpeta sistema_academico en VS Code.
3. Abra una terminal en esa carpeta.
4. Ejecute: python main.py

Arquitectura:
- models/models.py: ModeloBase, Persona, Estudiante, Materia y Matricula.
- views.py: reglas del negocio, validaciones y operaciones CRUD.
- main.py: menús, input() y print().
- shared/json_manager.py: lectura y escritura de archivos JSON.
- shared/validaciones.py: validación reutilizable de email y enteros.
- data/: persistencia JSON.

La carpeta data inicia vacía. Los registros se guardan automáticamente al usar el programa.
Las notas se califican de 0 a 20; se aprueba con 14 o más.
