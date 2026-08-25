#!/usr/bin/env python3
"""Verificación de sintaxis y dependencias para CI.

No instala el stack del proyecto: ast.parse valida la sintaxis sin evaluar los
import, así que no hace falta compilar pmdarima para saber si el código está bien.

Uso: python .github/scripts/check.py
"""

import ast
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# El nombre que se importa no siempre es el del paquete que se instala.
IMPORT_A_PAQUETE = {
    "dotenv": "python-dotenv",
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "PIL": "pillow",
    "yaml": "pyyaml",
}

fallos = []


def seccion(titulo):
    print(f"\n{titulo}")


def celdas_de_codigo(ruta):
    """Devuelve el código de cada celda, sin las líneas mágicas de IPython."""
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    for celda in nb.get("cells", []):
        if celda.get("cell_type") != "code":
            continue
        lineas = [l for l in "".join(celda["source"]).split("\n")
                  if not l.strip().startswith(("%", "!"))]
        yield "\n".join(lineas)


def imports_de(codigo):
    for nodo in ast.walk(ast.parse(codigo)):
        if isinstance(nodo, ast.Import):
            for alias in nodo.names:
                yield alias.name.split(".")[0]
        elif isinstance(nodo, ast.ImportFrom) and nodo.module and nodo.level == 0:
            yield nodo.module.split(".")[0]


def comprobar_sintaxis_python():
    """Valida los módulos y devuelve el código de los que se pudieron parsear."""
    seccion("Sintaxis de los módulos")
    legibles = []
    for ruta in sorted(RAIZ.glob("src/*.py")):
        rel = ruta.relative_to(RAIZ)
        try:
            codigo = ruta.read_text(encoding="utf-8")
            ast.parse(codigo)
            print(f"  {rel}: ok")
            legibles.append(codigo)
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"  {rel}: {e}")
            fallos.append(f"no parsea: {rel}")
    return legibles


def comprobar_notebooks():
    """Valida los notebooks y devuelve las celdas de los que se pudieron leer."""
    seccion("Notebooks")
    legibles = []
    for ruta in sorted(RAIZ.glob("notebooks/*.ipynb")):
        rel = ruta.relative_to(RAIZ)
        try:
            celdas = list(celdas_de_codigo(ruta))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  {rel}: JSON inválido, {e}")
            fallos.append(f"JSON inválido: {rel}")
            continue
        try:
            for codigo in celdas:
                ast.parse(codigo)
            print(f"  {rel}: ok, {len(celdas)} celdas de código")
            legibles.append(celdas)
        except SyntaxError as e:
            print(f"  {rel}: celda con error de sintaxis, {e}")
            fallos.append(f"celda no parsea: {rel}")
    return legibles


def leer_requirements():
    """Lee requirements.txt exigiendo UTF-8 y devuelve los paquetes declarados."""
    seccion("Formato de requirements.txt")
    ruta = RAIZ / "requirements.txt"
    try:
        # Este check existe porque el fichero llegó a estar guardado en UTF-16.
        contenido = ruta.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        print(f"  no decodifica como UTF-8: {e}")
        fallos.append("requirements.txt no está en UTF-8")
        return set()

    lineas = [l.strip() for l in contenido.splitlines()]
    lineas = [l for l in lineas if l and not l.startswith("#")]
    patron = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*((==|>=|<=|~=)[\w.]+)?$")
    invalidas = [l for l in lineas if not patron.match(l)]
    if invalidas:
        print(f"  líneas inválidas: {', '.join(invalidas)}")
        fallos.append("requirements.txt mal formado")
    else:
        print(f"  ok, {len(lineas)} dependencias declaradas")

    return {re.split(r"==|>=|<=|~=", l)[0].lower().replace("_", "-") for l in lineas}


def comprobar_dependencias(declaradas, modulos, notebooks):
    """Toda librería importada debe estar declarada.

    Este check existe porque fredapi y scipy ya se colaron sin declarar.
    Solo mira el código que parseó: lo que no parsea ya se reportó antes.
    """
    seccion("Dependencias declaradas")
    usadas = set()
    for codigo in modulos:
        usadas.update(imports_de(codigo))
    for celdas in notebooks:
        for codigo in celdas:
            usadas.update(imports_de(codigo))

    externas = {m for m in usadas if m not in sys.stdlib_module_names and m != "src"}
    normalizadas = {IMPORT_A_PAQUETE.get(m, m).lower().replace("_", "-") for m in externas}
    faltan = sorted(normalizadas - declaradas)

    if faltan:
        print(f"  usadas pero NO declaradas: {', '.join(faltan)}")
        fallos.append("faltan dependencias en requirements.txt")
    else:
        print(f"  ok, {len(externas)} librerías usadas y todas declaradas")


def main():
    if sys.version_info < (3, 10):
        sys.exit("Este script necesita Python 3.10+ (usa sys.stdlib_module_names)")

    modulos = comprobar_sintaxis_python()
    notebooks = comprobar_notebooks()
    declaradas = leer_requirements()
    comprobar_dependencias(declaradas, modulos, notebooks)

    print()
    if fallos:
        print("FALLO:")
        for f in fallos:
            print(f"  - {f}")
        sys.exit(1)
    print("Todo correcto.")


if __name__ == "__main__":
    main()
