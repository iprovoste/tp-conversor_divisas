"""Módulo encargado de consultar la API de cotizaciones y hacer cálculos."""

from datetime import datetime

import requests

URL_API: str = "https://dolarapi.com/v1/dolares"
TIEMPO_ESPERA: int = 10


class ErrorCotizacion(Exception):
    """Error propio para problemas al obtener o interpretar cotizaciones."""


def obtener_cotizaciones(url: str = URL_API) -> list[dict]:
    """Consulta la API y devuelve la lista de cotizaciones sin procesar.

    Args:
        url: Dirección de la API a consultar.

    Returns:
        Lista de diccionarios, uno por cada tipo de dólar.

    Raises:
        ErrorCotizacion: Si no hay conexión, la API falla o la respuesta
            no tiene el formato esperado.
    """
    try:
        respuesta = requests.get(url, timeout=TIEMPO_ESPERA)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except requests.ConnectionError as error:
        raise ErrorCotizacion(
            "No hay conexión a internet o la API no responde."
        ) from error
    except requests.Timeout as error:
        raise ErrorCotizacion(
            "La API tardó demasiado en responder."
        ) from error
    except requests.HTTPError as error:
        raise ErrorCotizacion(
            f"La API devolvió un error HTTP: {error}"
        ) from error
    except requests.RequestException as error:
        raise ErrorCotizacion(
            f"Error inesperado al consultar la API: {error}"
        ) from error
    except ValueError as error:
        raise ErrorCotizacion(
            "La respuesta de la API no es un JSON válido."
        ) from error

    if not isinstance(datos, list):
        raise ErrorCotizacion("La respuesta de la API no es una lista.")
    return datos


def convertir_precio(valor: object) -> float | None:
    """Convierte un precio de la API a número.

    Args:
        valor: Precio tal como viene en la API (número, texto o None).

    Returns:
        El precio como float, o None si no existe o no es un número
        positivo.
    """
    try:
        precio = float(valor)
    except (TypeError, ValueError):
        return None
    return precio if precio > 0 else None


def convertir_fecha(texto: object) -> datetime | None:
    """Convierte la fecha ISO de la API a la hora local de la máquina.

    Args:
        texto: Fecha en formato ISO 8601 (ej: "2026-11-03T18:00:00.000Z").

    Returns:
        La fecha en hora local, o None si no se puede interpretar.
    """
    if not isinstance(texto, str):
        return None
    try:
        fecha = datetime.fromisoformat(texto.replace("Z", "+00:00"))
    except ValueError:
        return None
    return fecha.astimezone()


def normalizar_cotizaciones(cotizaciones: list[dict]) -> list[dict]:
    """Limpia los datos de la API y deja solo las cotizaciones válidas.

    Una cotización es válida si tiene nombre y precio de venta. El precio
    de compra y la fecha pueden faltar (quedan en None).

    Args:
        cotizaciones: Lista cruda devuelta por la API.

    Returns:
        Lista de diccionarios con las claves nombre, compra, venta y fecha.

    Raises:
        ErrorCotizacion: Si no queda ninguna cotización válida.
    """
    normalizadas = []
    for cotizacion in cotizaciones:
        if not isinstance(cotizacion, dict):
            continue
        nombre = cotizacion.get("nombre")
        venta = convertir_precio(cotizacion.get("venta"))
        if not nombre or venta is None:
            continue
        normalizadas.append({
            "nombre": str(nombre),
            "compra": convertir_precio(cotizacion.get("compra")),
            "venta": venta,
            "fecha": convertir_fecha(cotizacion.get("fechaActualizacion")),
        })

    if not normalizadas:
        raise ErrorCotizacion("La API no devolvió cotizaciones válidas.")
    return normalizadas


def pesos_a_dolares(monto_ars: float, venta: float) -> float:
    """Convierte pesos a dólares usando el precio de venta.

    Se usa la venta porque es el precio al que se compran dólares con pesos.

    Args:
        monto_ars: Monto en pesos argentinos.
        venta: Precio de venta del dólar en pesos.

    Returns:
        Monto equivalente en dólares.
    """
    return monto_ars / venta


def dolares_a_pesos(monto_usd: float, compra: float) -> float:
    """Convierte dólares a pesos usando el precio de compra.

    Se usa la compra porque es el precio que pagan por los dólares
    cuando uno los vende.

    Args:
        monto_usd: Monto en dólares.
        compra: Precio de compra del dólar en pesos.

    Returns:
        Monto equivalente en pesos argentinos.
    """
    return monto_usd * compra


def calcular_conversiones(
    cotizaciones: list[dict],
    monto: float,
    a_dolares: bool,
) -> list[dict]:
    """Agrega a cada cotización el total convertido.

    Args:
        cotizaciones: Cotizaciones ya normalizadas.
        monto: Monto a convertir (en ARS o en USD según ``a_dolares``).
        a_dolares: True para convertir ARS → USD, False para USD → ARS.

    Returns:
        Copia de las cotizaciones con la clave extra "total". Vale None si
        falta el precio necesario para esa conversión.
    """
    resultados = []
    for cotizacion in cotizaciones:
        if a_dolares:
            total = pesos_a_dolares(monto, cotizacion["venta"])
        elif cotizacion["compra"] is not None:
            total = dolares_a_pesos(monto, cotizacion["compra"])
        else:
            total = None
        resultados.append({**cotizacion, "total": total})
    return resultados
