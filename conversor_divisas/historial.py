"""Módulo encargado de guardar y leer el historial de conversiones.

Cada conversión se guarda en dos archivos:
    - historial.csv: una fila por resultado, para abrir con Excel o
      para que el programa lo lea.
    - historial.txt: un bloque legible por conversión.
"""

import csv
from datetime import datetime
from pathlib import Path

from vista import formatear_numero

CARPETA: Path = Path(__file__).resolve().parent
ARCHIVO_CSV: Path = CARPETA / "historial.csv"
ARCHIVO_TXT: Path = CARPETA / "historial.txt"
CAMPOS: tuple[str, ...] = (
    "fecha", "origen", "monto", "destino", "cotizacion", "precio",
    "resultado",
)
FORMATO_FECHA: str = "%Y-%m-%d %H:%M:%S"


class ErrorHistorial(Exception):
    """Error propio para problemas al leer o escribir el historial."""


def armar_registros(
    resultados: list[dict],
    monto: float,
    desde_pesos: bool,
    fecha: datetime | None = None,
) -> list[dict]:
    """Arma las filas del historial a partir de una conversión.

    Args:
        resultados: Cotizaciones con las claves "precio" y "total".
        monto: Monto original ingresado por el usuario.
        desde_pesos: True si se convirtió ARS → moneda.
        fecha: Momento de la conversión (por defecto, ahora).

    Returns:
        Lista de diccionarios con las claves de ``CAMPOS``.
    """
    fecha_texto = (fecha or datetime.now()).strftime(FORMATO_FECHA)
    registros = []
    for fila in resultados:
        origen, destino = (
            ("ARS", fila["moneda"]) if desde_pesos else (fila["moneda"], "ARS")
        )
        registros.append({
            "fecha": fecha_texto,
            "origen": origen,
            "monto": round(monto, 2),
            "destino": destino,
            "cotizacion": fila["nombre"],
            "precio": "" if fila["precio"] is None else fila["precio"],
            "resultado": (
                "" if fila["total"] is None else round(fila["total"], 2)
            ),
        })
    return registros


def guardar_csv(registros: list[dict], archivo: Path = ARCHIVO_CSV) -> None:
    """Agrega los registros al final del archivo CSV.

    Si el archivo no existe o está vacío, primero escribe el encabezado.

    Args:
        registros: Filas a guardar.
        archivo: Ruta del archivo CSV.

    Raises:
        ErrorHistorial: Si no se puede escribir el archivo.
    """
    try:
        es_nuevo = not archivo.exists() or archivo.stat().st_size == 0
        with archivo.open("a", newline="", encoding="utf-8-sig") as salida:
            escritor = csv.DictWriter(salida, fieldnames=CAMPOS)
            if es_nuevo:
                escritor.writeheader()
            escritor.writerows(registros)
    except OSError as error:
        raise ErrorHistorial(
            f"No se pudo guardar el historial en {archivo.name}: {error}"
        ) from error


def guardar_txt(registros: list[dict], archivo: Path = ARCHIVO_TXT) -> None:
    """Agrega un bloque legible con la conversión al archivo de texto.

    Args:
        registros: Filas de una misma conversión.
        archivo: Ruta del archivo de texto.

    Raises:
        ErrorHistorial: Si no se puede escribir el archivo.
    """
    if not registros:
        return
    primero = registros[0]
    destinos = {registro["destino"] for registro in registros}
    destino = destinos.pop() if len(destinos) == 1 else "varias monedas"
    lineas = [
        f"[{primero['fecha']}] {formatear_numero(primero['monto'])} "
        f"{primero['origen']} → {destino}"
    ]
    for registro in registros:
        if registro["resultado"] == "":
            detalle = "sin cotización"
        else:
            detalle = (
                f"{formatear_numero(registro['resultado'])} "
                f"{registro['destino']} "
                f"(precio {formatear_numero(registro['precio'])})"
            )
        lineas.append(f"    {registro['cotizacion']}: {detalle}")

    try:
        with archivo.open("a", encoding="utf-8") as salida:
            salida.write("\n".join(lineas) + "\n\n")
    except OSError as error:
        raise ErrorHistorial(
            f"No se pudo guardar el historial en {archivo.name}: {error}"
        ) from error


def guardar_conversion(
    resultados: list[dict],
    monto: float,
    desde_pesos: bool,
) -> None:
    """Guarda una conversión en el historial CSV y en el TXT.

    Args:
        resultados: Cotizaciones con las claves "precio" y "total".
        monto: Monto original ingresado por el usuario.
        desde_pesos: True si se convirtió ARS → moneda.

    Raises:
        ErrorHistorial: Si no se puede escribir alguno de los archivos.
    """
    registros = armar_registros(resultados, monto, desde_pesos)
    guardar_csv(registros)
    guardar_txt(registros)


def leer_historial(
    cantidad: int = 20,
    archivo: Path = ARCHIVO_CSV,
) -> list[dict]:
    """Lee las últimas filas guardadas en el historial CSV.

    Args:
        cantidad: Cuántas filas devolver como máximo (las más recientes).
        archivo: Ruta del archivo CSV.

    Returns:
        Lista de diccionarios (valores como texto). Vacía si todavía no
        hay historial.

    Raises:
        ErrorHistorial: Si el archivo existe pero no se puede leer.
    """
    if not archivo.exists():
        return []
    try:
        with archivo.open(newline="", encoding="utf-8-sig") as entrada:
            filas = list(csv.DictReader(entrada))
    except (OSError, csv.Error, UnicodeDecodeError) as error:
        raise ErrorHistorial(
            f"No se pudo leer el historial de {archivo.name}: {error}"
        ) from error
    return filas[-cantidad:]
