"""Punto de entrada del Conversor de Divisas (ARS ⇄ USD)."""

from cotizaciones import (
    ErrorCotizacion,
    calcular_conversiones,
    normalizar_cotizaciones,
    obtener_cotizaciones,
)
from vista import (
    mostrar_error,
    mostrar_mensaje,
    mostrar_tabla,
    pedir_monto,
    pedir_opcion,
)


def cargar_cotizaciones() -> list[dict]:
    """Descarga las cotizaciones de la API y las deja listas para usar.

    Returns:
        Lista de cotizaciones normalizadas.

    Raises:
        ErrorCotizacion: Si no se pudieron obtener cotizaciones válidas.
    """
    return normalizar_cotizaciones(obtener_cotizaciones())


def convertir(cotizaciones: list[dict], a_dolares: bool) -> None:
    """Pide un monto, hace la conversión y muestra la tabla.

    Args:
        cotizaciones: Cotizaciones normalizadas.
        a_dolares: True para ARS → USD, False para USD → ARS.
    """
    monto = pedir_monto("pesos (ARS)" if a_dolares else "dólares (USD)")
    resultados = calcular_conversiones(cotizaciones, monto, a_dolares)
    mostrar_tabla(resultados, monto, a_dolares)


def main() -> None:
    """Coordina el programa: carga cotizaciones y atiende el menú."""
    print("💱 Conversor de Divisas — Cotización en vivo")
    try:
        cotizaciones = cargar_cotizaciones()
        mostrar_mensaje(f"Se cargaron {len(cotizaciones)} cotizaciones.")

        while True:
            opcion = pedir_opcion()
            if opcion == "0":
                print("\n👋 ¡Hasta luego!")
                break
            if opcion == "3":
                try:
                    cotizaciones = cargar_cotizaciones()
                    mostrar_mensaje("Cotizaciones actualizadas.")
                except ErrorCotizacion as error:
                    mostrar_error(f"{error} Se siguen usando las anteriores.")
                continue
            convertir(cotizaciones, a_dolares=(opcion == "1"))
    except ErrorCotizacion as error:
        mostrar_error(str(error))
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Programa cancelado por el usuario.")


if __name__ == "__main__":
    main()
