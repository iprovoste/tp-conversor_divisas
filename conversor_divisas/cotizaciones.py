"""Módulo encargado de consultar la API de cotizaciones y hacer cálculos."""

from datetime import datetime

import requests

URL_DOLARES: str = "https://dolarapi.com/v1/dolares"
URL_MONEDAS: str = "https://dolarapi.com/v1/cotizaciones"
TIEMPO_ESPERA: int = 10
CASA_REFERENCIA: str = "oficial"


class ErrorCotizacion(Exception):
    """Error propio para problemas al obtener o interpretar cotizaciones."""


def obtener_cotizaciones(url: str) -> list[dict]:
    """Consulta la API y devuelve la lista de cotizaciones sin procesar.

    Args:
        url: Dirección de la API a consultar.

    Returns:
        Lista de diccionarios, uno por cada cotización.

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

    Una cotización es válida si tiene nombre, código de moneda y precio de
    venta. El precio de compra y la fecha pueden faltar (quedan en None).

    Args:
        cotizaciones: Lista cruda devuelta por la API.

    Returns:
        Lista de diccionarios con las claves moneda, casa, nombre, compra,
        venta y fecha.

    Raises:
        ErrorCotizacion: Si no queda ninguna cotización válida.
    """
    normalizadas = []
    for cotizacion in cotizaciones:
        if not isinstance(cotizacion, dict):
            continue
        nombre = cotizacion.get("nombre")
        moneda = cotizacion.get("moneda")
        venta = convertir_precio(cotizacion.get("venta"))
        if not nombre or not moneda or venta is None:
            continue
        normalizadas.append({
            "moneda": str(moneda).upper(),
            "casa": str(cotizacion.get("casa", "")),
            "nombre": str(nombre),
            "compra": convertir_precio(cotizacion.get("compra")),
            "venta": venta,
            "fecha": convertir_fecha(cotizacion.get("fechaActualizacion")),
        })

    if not normalizadas:
        raise ErrorCotizacion("La API no devolvió cotizaciones válidas.")
    return normalizadas


def cargar_todo() -> dict[str, list[dict]]:
    """Descarga y normaliza las cotizaciones del dólar y de otras monedas.

    Returns:
        Diccionario con las claves "dolares" y "monedas".

    Raises:
        ErrorCotizacion: Si alguna de las dos consultas falla.
    """
    dolares = normalizar_cotizaciones(obtener_cotizaciones(URL_DOLARES))
    monedas = normalizar_cotizaciones(obtener_cotizaciones(URL_MONEDAS))
    return {"dolares": agregar_brecha(dolares), "monedas": monedas}


def calcular_brecha(venta: float, venta_referencia: float) -> float:
    """Calcula la brecha porcentual entre dos precios.

    Args:
        venta: Precio de venta a comparar.
        venta_referencia: Precio de venta de referencia (el oficial).

    Returns:
        Diferencia en porcentaje (ej: 6.3 significa un 6,3 % más caro).
    """
    return (venta / venta_referencia - 1) * 100


def agregar_brecha(
    cotizaciones: list[dict],
    casa_referencia: str = CASA_REFERENCIA,
) -> list[dict]:
    """Agrega a cada cotización su brecha contra la casa de referencia.

    Args:
        cotizaciones: Cotizaciones normalizadas del dólar.
        casa_referencia: Casa contra la que se compara (por defecto,
            "oficial").

    Returns:
        Copia de las cotizaciones con la clave extra "brecha". Vale None
        si no se encontró la casa de referencia.
    """
    referencia = next(
        (c for c in cotizaciones if c["casa"] == casa_referencia), None
    )
    resultado = []
    for cotizacion in cotizaciones:
        brecha = None
        if referencia is not None:
            brecha = calcular_brecha(cotizacion["venta"], referencia["venta"])
        resultado.append({**cotizacion, "brecha": brecha})
    return resultado


def pesos_a_moneda(monto_ars: float, venta: float) -> float:
    """Convierte pesos a otra moneda usando el precio de venta.

    Se usa la venta porque es el precio al que se compra la moneda con
    pesos.

    Args:
        monto_ars: Monto en pesos argentinos.
        venta: Precio de venta de la moneda en pesos.

    Returns:
        Monto equivalente en la otra moneda.
    """
    return monto_ars / venta


def moneda_a_pesos(monto: float, compra: float) -> float:
    """Convierte otra moneda a pesos usando el precio de compra.

    Se usa la compra porque es el precio que pagan por la moneda cuando
    uno la vende.

    Args:
        monto: Monto en la otra moneda.
        compra: Precio de compra de la moneda en pesos.

    Returns:
        Monto equivalente en pesos argentinos.
    """
    return monto * compra


def calcular_conversiones(
    cotizaciones: list[dict],
    monto: float,
    desde_pesos: bool,
) -> list[dict]:
    """Agrega a cada cotización el total convertido.

    Args:
        cotizaciones: Cotizaciones ya normalizadas.
        monto: Monto a convertir.
        desde_pesos: True para ARS → moneda, False para moneda → ARS.

    Returns:
        Copia de las cotizaciones con las claves extra "precio" (el precio
        usado) y "total". Ambas valen None si falta el precio necesario.
    """
    resultados = []
    for cotizacion in cotizaciones:
        precio = cotizacion["venta"] if desde_pesos else cotizacion["compra"]
        if precio is None:
            total = None
        elif desde_pesos:
            total = pesos_a_moneda(monto, precio)
        else:
            total = moneda_a_pesos(monto, precio)
        resultados.append({**cotizacion, "precio": precio, "total": total})
    return resultados


def buscar_moneda(monedas: list[dict], codigo: str) -> dict:
    """Busca una moneda por su código (ej: "EUR").

    Args:
        monedas: Cotizaciones normalizadas de las monedas.
        codigo: Código ISO de la moneda, en cualquier combinación de
            mayúsculas y minúsculas.

    Returns:
        La cotización de esa moneda.

    Raises:
        ErrorCotizacion: Si la moneda no está en la lista.
    """
    for moneda in monedas:
        if moneda["moneda"] == codigo.upper():
            return moneda
    raise ErrorCotizacion(f"No hay cotización para la moneda {codigo}.")
