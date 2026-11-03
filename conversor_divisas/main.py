"""Punto de entrada del Conversor de Divisas (ARS → USD oficial y blue)."""

from cotizaciones import (
    ErrorCotizacion,
    armar_resultados,
    filtrar_cotizaciones,
    obtener_cotizaciones,
)
from vista import mostrar_error, mostrar_tabla, pedir_monto


def main() -> None:
    """Coordina el programa: pide el monto, consulta la API y muestra."""
    print("💱 Conversor de Divisas — Cotización en vivo\n")
    try:
        monto = pedir_monto()
        cotizaciones = obtener_cotizaciones()
        seleccionadas = filtrar_cotizaciones(cotizaciones)
        resultados = armar_resultados(seleccionadas, monto)
        mostrar_tabla(resultados, monto)
    except ErrorCotizacion as error:
        mostrar_error(str(error))
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Programa cancelado por el usuario.")


if __name__ == "__main__":
    main()
