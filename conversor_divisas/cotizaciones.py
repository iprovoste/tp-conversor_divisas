"""Módulo encargado de consultar la API de cotizaciones y hacer cálculos."""

import requests

URL_API: str = "https://dolarapi.com/v1/dolares"
CASAS_BUSCADAS: tuple[str, ...] = ("oficial", "blue")
TIEMPO_ESPERA: int = 10


class ErrorCotizacion(Exception):
    """Error propio para problemas al obtener o interpretar cotizaciones."""


def obtener_cotizaciones(url: str = URL_API) -> list[dict]:
    """Consulta la API y devuelve la lista de cotizaciones.

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


def filtrar_cotizaciones(
    cotizaciones: list[dict],
    casas: tuple[str, ...] = CASAS_BUSCADAS,
) -> list[dict]:
    """Se queda solo con las cotizaciones de las casas pedidas.

    Args:
        cotizaciones: Lista completa devuelta por la API.
        casas: Nombres de las casas a conservar (ej: "oficial", "blue").

    Returns:
        Lista con las cotizaciones encontradas, en el orden de ``casas``.

    Raises:
        ErrorCotizacion: Si falta alguna de las casas buscadas.
    """
    por_casa = {
        cotizacion.get("casa"): cotizacion
        for cotizacion in cotizaciones
        if isinstance(cotizacion, dict)
    }
    faltantes = [casa for casa in casas if casa not in por_casa]
    if faltantes:
        raise ErrorCotizacion(
            f"No se encontraron cotizaciones para: {', '.join(faltantes)}"
        )
    return [por_casa[casa] for casa in casas]


def convertir(monto_ars: float, venta: float) -> float:
    """Convierte un monto en pesos a dólares usando el precio de venta.

    Args:
        monto_ars: Monto en pesos argentinos.
        venta: Precio de venta del dólar en pesos.

    Returns:
        Monto equivalente en dólares.

    Raises:
        ErrorCotizacion: Si el precio de venta no es un número positivo.
    """
    if venta <= 0:
        raise ErrorCotizacion("El precio de venta debe ser mayor a cero.")
    return monto_ars / venta


def armar_resultados(cotizaciones: list[dict], monto_ars: float) -> list[dict]:
    """Calcula la conversión para cada cotización.

    Args:
        cotizaciones: Cotizaciones ya filtradas.
        monto_ars: Monto en pesos a convertir.

    Returns:
        Lista de diccionarios con nombre, compra, venta y total en USD.

    Raises:
        ErrorCotizacion: Si a alguna cotización le faltan datos o no son
            numéricos.
    """
    resultados = []
    for cotizacion in cotizaciones:
        try:
            nombre = str(cotizacion["nombre"])
            compra = float(cotizacion["compra"])
            venta = float(cotizacion["venta"])
        except KeyError as error:
            raise ErrorCotizacion(
                f"A la cotización le falta el dato {error}."
            ) from error
        except (TypeError, ValueError) as error:
            raise ErrorCotizacion(
                "La cotización tiene valores que no son numéricos."
            ) from error

        resultados.append({
            "nombre": nombre,
            "compra": compra,
            "venta": venta,
            "total_usd": convertir(monto_ars, venta),
        })
    return resultados
